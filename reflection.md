# PawPal+ Project Reflection

## 1. System Design

The three core actions a user should be able to perform are to set up their information and their pets information, outline any constraints or scheduling details or specific tasks, and view and edit the final task schedule.

The main objects for the system I believe should be the User (holds user information like name and scheduling constraints; performs modifications to its fields), Pet (holds pet name, needs, and time sensitive information; performs modifications to its fields and creation/deletion of itself), Task (holds the task name, description, time sensitive information; performs text modifications to its fields and creation/deletion of itself), Day (holds the day name, tasks during that day; performs modifications to its fields, sorting by time). 

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

I have User, Pet, Task, and Day classes. The responsibilities are as follows: User- defines the user, their availability, and their pets. Pet- defines the pet and required tasks, Task - defines the task such as completion status and timing, and Day- describes the tasks in the day which can be modified and sorted. 

**b. Design changes**

- Did your design change during implementation? 
Yes 
- If yes, describe at least one change and why you made it.
One change is that tasks do not link back to the pet that needs that task done. If a user has multiple pets and only one needs medication, there's no link back to the pet that needs that task enacted on it. So the change is to set the task with the pet name when you add a task to the pet. 
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
The conflict detection compares every task's preferred time-slot against other tasks, catching both exact-time matches and overlapping durations. The tradeoff is that it only examines tasks that have a preferred_time set. The tasks without one are placed dynamically by generate_schedule and are never flagged as conflicts. 

- Why is that tradeoff reasonable for this scenario?
This is reasonable because tasks without a preferred time have no user-specified constraint to violate so the scheduler is free to place them wherever a gap exists so conflict has no meaningful definition for them.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
I used Claude to collaboratively brainstorm and create the UML diagram, revise it at my will, come up with implementations and asked it to ask me for approval before fully implementing it. I also used it for debugging errors if things weren't running and had it describe the issue to me and also refactoring things requested in the project description. i also used it to generate long pieces of documentation in the readme and some docstrings.

- What kinds of prompts or questions were most helpful?
Asking it to explain things to me in plan mode before implementing it was helpful to me to understand new information and to reduce the amount of prompting to get a final product i was happy with. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
The AI suggested some attributes to be set in the Pet class such as species, age, etc. I thought that was too complex at the moment and an unnecessary addition to the app that was purely cosmetic.

- How did you evaluate or verify what the AI suggested?
I used my own judgement to find that it would be unnecessary and then I highlighted it as context and asked why it suggested it and that confirmed that I did not need to accept the suggestion. 
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
