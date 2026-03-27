import streamlit as st
from pawpal_system import Owner, Pet, Task, Priority, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# --- Session state setup ---
# Streamlit reruns the whole script on every interaction.
# Storing owner here means it survives button clicks and page refreshes.
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

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority_str = st.selectbox("Priority", ["high", "medium", "low"])

    priority_map = {"high": Priority.HIGH, "medium": Priority.MEDIUM, "low": Priority.LOW}

    if st.button("Add task"):
        task = Task(
            title=task_title,
            duration_minutes=int(duration),
            priority=priority_map[priority_str],
            category="general",
        )
        pet.add_task(task)
        st.success(f"Added: {task_title}")

    if pet.tasks:
        st.write(f"Tasks for {pet.name}:")
        st.table([
            {"Title": t.title, "Duration (min)": t.duration_minutes, "Priority": t.priority.name}
            for t in pet.tasks
        ])
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
            st.success("Here's today's plan:")
            st.text(plan.summary())
