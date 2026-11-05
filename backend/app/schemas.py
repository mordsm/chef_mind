from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class KnowledgeUnit(StrictModel):
    knowledge_id: str = Field(min_length=1, max_length=80, pattern=r"^[a-zA-Z0-9_-]+$")
    title: str = Field(min_length=1, max_length=200)
    principle: str = Field(min_length=1, max_length=2000)
    conditions: list[str] = Field(default_factory=list, max_length=20)
    observations: list[str] = Field(min_length=1, max_length=20)
    recommended_action: str = Field(min_length=1, max_length=1200)
    exceptions: list[str] = Field(default_factory=list, max_length=20)
    safety_notes: list[str] = Field(default_factory=list, max_length=20)
    kashrut_notes: list[str] = Field(default_factory=list, max_length=20)
    tags: list[str] = Field(min_length=1, max_length=20)
    confidence: int = Field(ge=0, le=100)
    verified_on: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    # A conflicting candidate cannot activate until the reviewer resolves it.
    conflicts_with: list[str] = Field(default_factory=list, max_length=20)
    required_ingredients: list[str] = Field(default_factory=list, max_length=20)

    @field_validator("conditions", "observations", "exceptions", "safety_notes", "kashrut_notes", "tags")
    @classmethod
    def bounded_items(cls, values):
        if any(not v or len(v) > 1000 for v in values):
            raise ValueError("List entries must be nonempty and at most 1000 characters")
        return values


class KnowledgeDocument(StrictModel):
    source_id: str = Field(min_length=1, max_length=80, pattern=r"^[a-zA-Z0-9_-]+$")
    title: str = Field(min_length=1, max_length=200)
    source_reference: str = Field(min_length=1, max_length=2000)
    license_status: Literal["original", "permission_granted", "open_license", "unknown"]
    license_reference: str = Field(min_length=1, max_length=2000)
    attribution: str = Field(default="", max_length=2000)
    adaptation_notes: str = Field(default="", max_length=2000)
    units: list[KnowledgeUnit] = Field(min_length=1, max_length=30)

    @field_validator("units")
    @classmethod
    def unique_ids(cls, units):
        if len({u.knowledge_id for u in units}) != len(units):
            raise ValueError("knowledge_id must be unique within a document")
        return units


class ImportRequest(StrictModel):
    path: str = Field(min_length=1, max_length=500)
    idempotency_key: str = Field(min_length=8, max_length=100)


class ReviewRequest(StrictModel):
    expected_revision: int = Field(ge=1)
    reason: str = Field(min_length=3, max_length=1000)


class LifecycleRequest(StrictModel):
    expected_active_revision_id: str | None = Field(max_length=36)
    reason: str = Field(min_length=3, max_length=1000)


class InventoryItem(StrictModel):
    name: str = Field(min_length=1, max_length=160)
    quantity: float | None = Field(default=None, ge=0, allow_inf_nan=False)
    unit: str = Field(default="", max_length=40)
    verified: bool = False
    food_class: Literal["meat", "dairy", "pareve", "unknown"] = "unknown"
    allergens: list[str] = Field(default_factory=list, max_length=30)
    label_verified: bool = False


class Profile(StrictModel):
    forbid_meat_dairy: bool = True
    allergies: list[str] = Field(default_factory=list, max_length=30)
    experience: Literal["beginner", "intermediate", "advanced"] = "beginner"
    explanation: Literal["short", "extended", "quiet"] = "short"


class InventoryUpdate(StrictModel):
    items: list[InventoryItem] = Field(default_factory=list, max_length=100)


class CookingState(StrictModel):
    current_goal: str = Field(min_length=1, max_length=500)
    current_step: str = Field(default="", max_length=1200)
    reports: list[str] = Field(default_factory=list, max_length=30)
    safety_question: bool = False
    # This MVP does not autonomously time, observe or operate equipment.


class ChefRequest(StrictModel):
    cooking_id: str = Field(min_length=1, max_length=80, pattern=r"^[a-zA-Z0-9_-]+$")
    expected_state_revision: int = Field(default=0, ge=0)
    message: str = Field(min_length=1, max_length=2000)
    profile: Profile = Field(default_factory=Profile)
    confirm_profile_change: bool = False
    allow_external_model: bool = False
    state: CookingState
    inventory: list[InventoryItem] = Field(default_factory=list, max_length=100)
    essential_ingredients: list[str] = Field(default_factory=list, max_length=30)
    compare_techniques: bool = False
    confirmed_conditions: list[str] = Field(default_factory=list, max_length=20)


class Citation(StrictModel):
    source_id: str
    source_reference: str
    revision: int
    revision_id: str
    knowledge_id: str
    supporting_text: str
    attribution: str = ""
    license_reference: str = ""


class ChefDecision(StrictModel):
    station_protocol: dict = Field(default_factory=dict)
    basic_knowledge: list[dict[str, str]] = Field(default_factory=list)
    decision_type: Literal["action", "clarify", "blocked", "insufficient_evidence"]
    current_goal: str
    instruction: str
    culinary_reason: str
    success_signal: str
    estimated_check_time: int | None = None
    requires_confirmation: bool = True
    safety_flags: list[str] = Field(default_factory=list)
    inventory_assumptions: list[str] = Field(default_factory=list)
    response_text: str
    proposed_action: str | None = None
    rationale: str
    confidence: int = Field(ge=0, le=100)
    citations: list[Citation] = Field(default_factory=list)
    policy_flags: list[str] = Field(default_factory=list)
    alternatives: list[str] = Field(default_factory=list)
    state_revision: int = 0
    constitution_version: str = "0.1"
    constitution_digest: str = ""
    policy_version: str = "baseline-0.1"
    engine_version: str = "extractive-hash-v1"
    provider_status: str = "not_requested"
    provider_latency_ms: int | None = None
    missing_conditions: list[str] = Field(default_factory=list)
    available_topics: list[str] = Field(default_factory=list)
