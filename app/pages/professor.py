import reflex as rx
from app.components.sidebar import page_layout
from app.states.professor_state import ProfessorState
from app.states.auth_state import AuthState


def student_card(student) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.image(
                src=f"https://api.dicebear.com/9.x/initials/svg?seed={student['name']}",
                class_name="w-12 h-12 rounded-full",
            ),
            rx.el.div(
                rx.el.h3(student["name"], class_name="font-semibold text-gray-800"),
                rx.el.p(student["email"], class_name="text-sm text-gray-500"),
                class_name="ml-4",
            ),
            class_name="flex items-center",
        ),
        rx.el.button(
            "Voir les notes",
            on_click=lambda: ProfessorState.select_student(student["id"]),
            class_name="px-4 py-2 bg-teal-500 text-white rounded-xl hover:bg-teal-600 transition-all duration-200",
        ),
        class_name="flex items-center justify-between p-6 bg-white rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition-all duration-300",
    )


def grade_row(grade, student_id: int) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            grade["subject"], class_name="px-6 py-4 text-sm text-gray-800 font-medium"
        ),
        rx.el.td(
            f"{grade['grade']:.1f} / 20",
            class_name="px-6 py-4 text-sm font-semibold text-teal-600",
        ),
        rx.el.td(grade["coefficient"], class_name="px-6 py-4 text-sm text-gray-600"),
        rx.el.td(grade["date"], class_name="px-6 py-4 text-sm text-gray-600"),
        rx.el.td(grade["semester"], class_name="px-6 py-4 text-sm text-gray-600"),
        rx.el.td(
            rx.el.button(
                rx.icon("disc_3", class_name="w-4 h-4"),
                on_click=ProfessorState.toggle_edit_mode,
                class_name="p-2 text-gray-500 hover:text-teal-600 hover:bg-teal-50 rounded-lg transition-all duration-200",
            ),
            class_name="px-6 py-4",
        ),
        class_name="hover:bg-gray-50 transition-colors duration-200",
    )


def edit_grade_form() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Modifier une note", class_name="text-xl font-bold text-gray-800 mb-6"
            ),
            rx.el.form(
                rx.el.input(
                    type="hidden",
                    name="student_id",
                    default_value=ProfessorState.selected_student_id.to_string(),
                ),
                rx.el.div(
                    rx.el.label(
                        "Matière",
                        class_name="block text-sm font-semibold text-gray-700 mb-2",
                    ),
                    rx.el.select(
                        rx.el.option(
                            "Sélectionnez une matière", value="", disabled=True
                        ),
                        rx.foreach(
                            ProfessorState.subjects_taught,
                            lambda subject: rx.el.option(subject, value=subject),
                        ),
                        name="subject",
                        required=True,
                        class_name="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500 focus:border-transparent",
                    ),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.el.label(
                        "Nouvelle note (sur 20)",
                        class_name="block text-sm font-semibold text-gray-700 mb-2",
                    ),
                    rx.el.input(
                        type="number",
                        name="new_grade",
                        step="0.1",
                        min="0",
                        max="20",
                        required=True,
                        placeholder="Ex: 15.5",
                        class_name="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500 focus:border-transparent",
                    ),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.el.button(
                        "Annuler",
                        type="button",
                        on_click=ProfessorState.toggle_edit_mode,
                        class_name="px-6 py-3 bg-gray-200 text-gray-800 rounded-xl hover:bg-gray-300 transition-all duration-200 mr-4",
                    ),
                    rx.el.button(
                        rx.cond(
                            ProfessorState.is_updating,
                            rx.spinner(class_name="w-5 h-5 text-white"),
                            "Mettre à jour",
                        ),
                        type="submit",
                        is_disabled=ProfessorState.is_updating,
                        class_name="px-6 py-3 bg-teal-500 text-white rounded-xl hover:bg-teal-600 transition-all duration-200 flex items-center",
                    ),
                    class_name="flex justify-end",
                ),
                on_submit=ProfessorState.update_grade,
            ),
            class_name="bg-white p-8 rounded-2xl border border-gray-100 shadow-lg max-w-2xl mx-auto",
        ),
        class_name="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50",
    )


def student_grades_detail() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.button(
                rx.icon("arrow-left", class_name="w-5 h-5 mr-2"),
                "Retour à la liste",
                on_click=lambda: ProfessorState.select_student(0),
                class_name="flex items-center px-4 py-2 text-teal-600 hover:bg-teal-50 rounded-xl transition-all duration-200 mb-6",
            ),
            rx.el.div(
                rx.el.div(
                    rx.image(
                        src=f"https://api.dicebear.com/9.x/initials/svg?seed={ProfessorState.selected_student['name']}",
                        class_name="w-16 h-16 rounded-full",
                    ),
                    rx.el.div(
                        rx.el.h2(
                            ProfessorState.selected_student["name"],
                            class_name="text-2xl font-bold text-gray-800",
                        ),
                        rx.el.p(
                            ProfessorState.selected_student["email"],
                            class_name="text-gray-500",
                        ),
                        class_name="ml-6",
                    ),
                    class_name="flex items-center",
                ),
                rx.el.button(
                    rx.icon("plus", class_name="w-5 h-5 mr-2"),
                    "Ajouter une note",
                    on_click=ProfessorState.toggle_edit_mode,
                    class_name="flex items-center px-6 py-3 bg-teal-500 text-white rounded-xl hover:bg-teal-600 transition-all duration-200",
                ),
                class_name="flex justify-between items-center mb-8",
            ),
            class_name="mb-8",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Matière",
                            class_name="px-6 py-4 text-left text-sm font-semibold text-gray-700 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Note",
                            class_name="px-6 py-4 text-left text-sm font-semibold text-gray-700 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Coefficient",
                            class_name="px-6 py-4 text-left text-sm font-semibold text-gray-700 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Date",
                            class_name="px-6 py-4 text-left text-sm font-semibold text-gray-700 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Semestre",
                            class_name="px-6 py-4 text-left text-sm font-semibold text-gray-700 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Actions",
                            class_name="px-6 py-4 text-left text-sm font-semibold text-gray-700 uppercase tracking-wider",
                        ),
                        class_name="bg-gray-50 border-b border-gray-200",
                    )
                ),
                rx.el.tbody(
                    rx.foreach(
                        ProfessorState.selected_student["grades"],
                        lambda grade: grade_row(
                            grade, ProfessorState.selected_student_id
                        ),
                    ),
                    class_name="bg-white divide-y divide-gray-200",
                ),
                class_name="min-w-full",
            ),
            class_name="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden",
        ),
        rx.cond(ProfessorState.edit_mode, edit_grade_form()),
    )


def professor_dashboard() -> rx.Component:
    return page_layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    f"Professeur - {AuthState.current_user['name']}",
                    class_name="text-3xl font-bold text-gray-800 mb-2",
                ),
                rx.el.p(
                    "Gérez les notes de vos étudiants", class_name="text-gray-500 mb-8"
                ),
                class_name="mb-8",
            ),
            rx.cond(
                ProfessorState.selected_student_id == 0,
                rx.el.div(
                    rx.el.h2(
                        "Mes Étudiants",
                        class_name="text-2xl font-bold text-gray-800 mb-6",
                    ),
                    rx.el.div(
                        rx.foreach(ProfessorState.students_grades, student_card),
                        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
                    ),
                ),
                student_grades_detail(),
            ),
        )
    )