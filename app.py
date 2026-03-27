import streamlit as st
from pawpal_system import Owner, Pet, Task, Priority, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

if "owner" not in st.session_state:
    st.session_state.owner = None

# --- Owner & pet setup ---
st.subheader("Owner & Pet Info")

col1, col2, col3 = st.columns(3)
with col1:
    owner_name = st.text_input("Owner name", value="Jordan")
with col2:
    pet_name = st.text_input("Pet name", value="Mochi")
with col3:
    species = st.selectbox("Species", ["dog", "cat", "other"])

available_minutes = st.number_input("Available minutes today", min_value=10, max_value=480, value=90)

if st.button("Save owner & pet"):
    pet = Pet(name=pet_name, species=species, age=0)
    owner = Owner(name=owner_name)
    owner.add_pet(pet)
    st.session_state.owner = owner
    st.success(f"Saved! {owner_name} and {pet_name} are ready.")

# --- Task management ---
st.divider()
st.subheader("Tasks")

if st.session_state.owner is None:
    st.info("Save your owner and pet info above before adding tasks.")
else:
    pet = st.session_state.owner.pets[0]

    with st.form("add_task_form", clear_on_submit=True):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            task_title = st.text_input("Task title", value="Morning walk")
        with col2:
            duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
        with col3:
            priority_str = st.selectbox("Priority", ["high", "medium", "low"])
        with col4:
            frequency = st.selectbox("Frequency", ["daily", "weekly", "once"])
        deadline_hour = st.number_input("Deadline hour (optional, 0 = none)", min_value=0, max_value=23, value=0)
        submitted = st.form_submit_button("Add task")

    if submitted:
        priority_map = {"high": Priority.HIGH, "medium": Priority.MEDIUM, "low": Priority.LOW}
        task = Task(
            title=task_title,
            duration_minutes=int(duration),
            priority=priority_map[priority_str],
            category="general",
            frequency=frequency,
            deadline_hour=int(deadline_hour) if deadline_hour > 0 else None,
        )
        pet.add_task(task)
        st.success(f"Added: {task_title}")

    if pet.tasks:
        scheduler = Scheduler(owner=st.session_state.owner, available_minutes=int(available_minutes))
        sorted_tasks = scheduler.sort_by_time(pet.tasks)

        st.markdown(f"**Tasks for {pet.name}** — sorted by deadline:")
        st.table([
            {
                "Title": t.title,
                "Duration (min)": t.duration_minutes,
                "Priority": t.priority.name,
                "Deadline": f"{t.deadline_hour}:00" if t.deadline_hour else "—",
                "Frequency": t.frequency,
                "Done": "✅" if t.completed else "⬜",
            }
            for t in sorted_tasks
        ])

        col_a, col_b = st.columns(2)
        with col_a:
            pending = scheduler.filter_by_status(completed=False)
            st.metric("Pending tasks", len(pending))
        with col_b:
            done = scheduler.filter_by_status(completed=True)
            st.metric("Completed today", len(done))
    else:
        st.info("No tasks yet. Add one above.")

    # --- Schedule generation ---
    st.divider()
    st.subheader("Generate Schedule")

    if st.button("Generate schedule"):
        if not pet.tasks:
            st.warning("Add at least one task before generating a schedule.")
        else:
            scheduler = Scheduler(owner=st.session_state.owner, available_minutes=int(available_minutes))
            plan = scheduler.generate_plan()

            if plan.conflicts:
                for conflict in plan.conflicts:
                    st.warning(f"⚠️ {conflict}")

            if plan.slots:
                st.success(f"Plan for {plan.plan_date.strftime('%A, %B %d %Y')} — {plan.total_minutes_used} min used")
                st.table([
                    {
                        "Time": slot.start_time,
                        "Task": slot.task.title,
                        "Duration (min)": slot.task.duration_minutes,
                        "Why": slot.reason,
                    }
                    for slot in plan.slots
                ])
            else:
                st.error("No tasks could be scheduled — all tasks either exceed your time budget or are already done.")

            if plan.skipped_tasks:
                with st.expander(f"Skipped tasks ({len(plan.skipped_tasks)})"):
                    for task in plan.skipped_tasks:
                        st.write(f"• {task.title} ({task.duration_minutes} min) — didn't fit in budget")
