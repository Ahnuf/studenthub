// The six-hue course palette (see design tokens in globals.css).
// A course's color is derived from its id, not assigned randomly
// per render -- so "Thermodynamics" is always the same color on
// the timetable, on an assignment card, on a note, everywhere,
// without needing to store a color field on the backend.
const COURSE_COLORS = [
  "var(--course-terracotta)",
  "var(--course-sage)",
  "var(--course-dusty-blue)",
  "var(--course-plum)",
  "var(--course-ochre)",
  "var(--course-slate)",
] as const;

export function courseColor(courseId: number | string): string {
  const numericId =
    typeof courseId === "number"
      ? courseId
      : Array.from(String(courseId)).reduce(
          (sum, char) => sum + char.charCodeAt(0),
          0
        );

  return COURSE_COLORS[numericId % COURSE_COLORS.length];
}
