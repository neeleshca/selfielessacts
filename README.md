# CC_SelfieLessActs
Assignment/Project for the cloud computing (UE16CS352) course. This makes heavy use of AWS services, hence steps to reproduce are not present.<br>
The goal of this project was to create a backend for a photo uploading application. The backend should be scalable and fault-tolerant. To make sure it is scalable, we have implemented autoscaling, where more containers get spun if needed. Load balancing is implemented for the same. Fault tolerance is implemented using a heartbeat health check, where the container is replaced if unhealthy.<br>
The images are compressed and stored as a base64 string. No database is used.<br>
The backend API's had to handle functionality like pagination.<br>
