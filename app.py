import streamlit as st
from pawpal_system import User, Pet, Task, Day

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# --- Session state initialization (check-before-create) ---
if "owner" not in st.session_state:
    st.session_state.owner = User("Jordan")

owner = st.session_state.owner

# --- Owner setup ---
st.subheader("Owner Info")
owner_name = st.text_input("Owner name", value=owner.name)
if owner_name != owner.name:
    owner.set_name(owner_name)

col_start, col_end = st.columns(2)
with col_start:
    avail_start = st.text_input("Available from (HH:MM)", value=owner.available_start)
with col_end:
    avail_end = st.text_input("Available until (HH:MM)", value=owner.available_end)
if avail_start != owner.available_start or avail_end != owner.available_end:
    owner.set_availability(avail_start, avail_end)

st.divider()

# --- Add a pet ---
st.subheader("Pets")
new_pet_name = st.text_input("Pet name", value="")
if st.button("Add pet") and new_pet_name:
    owner.add_pet(Pet(name=new_pet_name))

if owner.pets:
    for pet in owner.pets:
        st.markdown(f"**{pet.name}** — {len(pet.tasks)} task(s)")
else:
    st.info("No pets yet. Add one above.")

st.divider()

# --- Add a task to a pet ---
st.subheader("Tasks")

if owner.pets:
    pet_names = [p.name for p in owner.pets]
    selected_pet = st.selectbox("Assign task to pet", pet_names)

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["high", "medium", "low"], index=0)

    preferred_time = st.text_input("Preferred time (HH:MM, optional)", value="")

    if st.button("Add task") and task_title:
        pet = next(p for p in owner.pets if p.name == selected_pet)
        pet.add_task(Task(
            title=task_title,
            duration_minutes=int(duration),
            priority=priority,
            preferred_time=preferred_time,
        ))

    for pet in owner.pets:
        if pet.tasks:
            st.markdown(f"**{pet.name}'s tasks:**")
            st.table([
                {"Task": t.title, "Duration": f"{t.duration_minutes} min",
                 "Priority": t.priority, "Time": t.preferred_time or "-"}
                for t in pet.tasks
            ])
else:
    st.info("Add a pet first, then you can assign tasks.")

st.divider()

# --- Generate schedule ---
st.subheader("Today's Schedule")

if st.button("Generate schedule"):
    all_tasks = [t for pet in owner.pets for t in pet.tasks]
    if not all_tasks:
        st.warning("No tasks to schedule. Add pets and tasks first.")
    else:
        today = Day(
            name="Today",
            start_time=owner.available_start,
            end_time=owner.available_end,
        )
        for task in all_tasks:
            today.add_task(task)
        st.code(today.explain_plan())
