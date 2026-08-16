import { courseColor } from "@/lib/course-colors";

export default function CourseTag({
  courseKey,
  label,
}: {
  courseKey: string | number;
  label: string;
}) {
  const color = courseColor(courseKey);

  return (
    <span className="course-tab" style={{ background: `${color}1a` }}>
      <span className="course-tab-dot" style={{ background: color }} />
      {label}
    </span>
  );
}
