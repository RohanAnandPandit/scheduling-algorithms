# scheduling-algorithms

### Creating a job
A job can be defined using the job index, processing time and optionally 
assign a release time, due date and weight.
You can also create an Idle job to force idleness.

### Adding jobs to a machine
A machine contains the list of jobs that need to be processed.
The machine can be initialised with a job list or the jobs can be added individually.
The machine is idle until the next job is released.

### Creating a Schedule
You can create a schedule with parallel machines.
Then you can add jobs to a machine at a specific index or the first available machine.

### Using the Scheduler
A Scheduler object has an internal Schedule. 
When you use an algorithm for a list of jobs, the corresponding method returns the schedule.
