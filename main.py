def build_classify_ui(selected_topics, target_drug, target_topic, target_cls, target_sub, is_exam):
    # Состояние
    state = {
        "topic": selected_topics[0] if len(selected_topics) == 1 else None,
        "class": None,
        "sub": None,
        "sel": None,
        "rec": None,
        "locked": False,
        "fb_text": "",
        "fb_color": "#333"
    }

    # Элементы интерфейса (создаём один раз)
    pb = ft.ProgressBar(value=0, color="#2ECC71", bgcolor="#FFCDD2", width=600)
    lbl_prog = ft.Text("", size=12)

    dd_topic = ft.Dropdown(label="Тема", width=500, options=[ft.dropdown.Option(key=t, text=t) for t in selected_topics])
    dd_class = ft.Dropdown(label="Класс", width=500, disabled=True)
    dd_sub = ft.Dropdown(label="Подкласс/Механизм", width=500, disabled=True)
    dd_sel = ft.Dropdown(
        label="Селективность",
        width=500,
        options=[
            ft.dropdown.Option(key="-", text="-"),
            ft.dropdown.Option(key="Селективный", text="Селективный"),
            ft.dropdown.Option(key="Неселективный", text="Неселективный")
        ]
    )
    dd_rec = ft.Dropdown(
        label="Рецепторы",
        width=500,
        options=[ft.dropdown.Option(key=x, text=x) for x in ["-", "α1", "α2", "α1, α2", "β1", "β2", "β1, β2", "β3", "М", "Н", "М, Н"]]
    )

    feedback = ft.Text("", weight=ft.FontWeight.BOLD, size=16, text_align=ft.TextAlign.CENTER)
    btn_check = ft.Button(content="Проверить", bgcolor="#F39C12", color="#FFF", width=200)
    btn_next = ft.Button(content="Далее", bgcolor="#2ECC71", color="#FFF", width=200, visible=False)

    def update_progress():
        dc, tc = calc_progress(stats, selected_topics, "class")
        pc = dc / tc if tc > 0 else 0
        pb.value = pc
        lbl_prog.value = f"Освоено: {dc} из {tc} ({int(pc*100)}%)"

    def update_class_options():
        if not state["topic"]:
            dd_class.options = []
            dd_class.value = None
            dd_class.disabled = True
            dd_sub.options = []
            dd_sub.value = None
            dd_sub.disabled = True
            return

        classes = list(DATABASE[state["topic"]].keys())
        dd_class.options = [ft.dropdown.Option(key=c, text=c) for c in classes]
        dd_class.disabled = state["locked"]
        dd_class.value = state["class"]

        # Обновляем подкласс
        update_sub_options()

    def update_sub_options():
        if not state["topic"] or not state["class"]:
            dd_sub.options = []
            dd_sub.value = None
