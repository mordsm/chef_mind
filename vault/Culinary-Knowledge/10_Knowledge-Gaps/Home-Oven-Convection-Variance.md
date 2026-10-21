---
id: GAP-EQP-001
type: knowledge_gap
name: Home Oven Convection & Thermostat Variance
domain: equipment
severity: HIGH
status: OPEN
impacted_concepts:
  - "[[Heat-Transfer]]"
  - "[[Core-Probe-Thermometry]]"
research_priority: P1
blocking_decisions:
  - "חיזוי זמן צלייה מדויק בדקות ללא מדידת טמפרטורת ליבה בתנור ביתי"
required_data_type: EMPIRICAL_MEASUREMENT
suggested_sources:
  - "מדידת כיול תרמוסטט ומדחום ליבה בזמן אמת"
created_at: 2026-10-21
updated_at: 2026-10-21
---

# שונות שטף החום וכיול בתנורים ביתיים (Home Oven Convection & Thermostat Variance)

## 1. ניסוח השאלה הפתוחה (The Open Question)
תנורים ביתיים סובלים מסטייה של $\pm 15^\circ\text{C}–25^\circ\text{C}$ ביחס לטמפרטורת החוגה וממחזורי הדלקה/כיבוי רחבים (Hysteresis). ללא מדידה פנימית, לא ניתן לגזור זמן בישול אוניברסלי ממרשם כתוב.

## 2. השפעה על מנוע ההחלטות (`chef_mind`)
מנוע השף לעולם אינו מאשר מוכנות או בטיחות של עוף, בשר או דג על סמך זמן תנור בלבד, אלא דורש תצפית מרקם ומדידת טמפרטורת ליבה (`[[Core-Probe-Thermometry]]`).
