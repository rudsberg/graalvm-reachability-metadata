# Turn off optimization and shrinking, we only want obfuscation
-dontoptimize
-dontshrink

# Basic options
-dontusemixedcaseclassnames
-verbose

# Keep classes from reflect-config.json
-keep class org_jooq.jooq.model.tables.records.CourseMaterialRecord
-keep class org_jooq.jooq.model.tables.records.CourseRecord
-keep class org_jooq.jooq.model.tables.records.StudentCourseRecord
-keep class org_jooq.jooq.model.tables.records.StudentCourseRecord
-keep class org_jooq.jooq.model.tables.records.StudentCourseRecord
-keep class org_jooq.jooq.model.tables.records.StudentRecord
-keep class org_jooq.jooq.model.tables.records.TeacherRecord