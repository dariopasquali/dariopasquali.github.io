## DevOps: development process automation (*Master Dissertation*)
<img src="../images/devops.png" width="100%"/>

[DevOps](https://devops.com/definition-devops-masses/) is like a philosophy. It's a way to see the development process putting the **people** in the center.

All the team is responsible for the development, deployment and mainteance of the company's product. DevOps propose a set of pratice to break the barriers between **developers** and **operations** in order to:
* Imporve the choesion of the team
* Automatize the development process, minimizing the required work
* Improve the quality of the final product.

The main mantra is:

---

### *<center> You build it. You run it. </center>*

---

Every member is responibile of what he develops during its entire life (from design to mainteance).

---

### Movie Recommender

I worked on a DevOps POC during my master degree internship in Milan. The idea was the automation of a movie recommender from [MovieLens](https://movielens.org/) dataset based on user preferences and ratings.

The result is a working project and a 16 hours course with [slides](https://github.com/endless-upgrade/DevOpsHours) and guided exectises. All the material is available in [endless-upgrade](https://github.com/endless-upgrade).

#### Architecture

All the code was hosed on Google Cloud Platform and written in Scala with [Spark](https://spark.apache.org/). The data elaboration is structured on 2 layers and based on [Cloudera CDH](https://www.cloudera.com/products/open-source/apache-hadoop/key-cdh-components.html)

##### ETL
Movielens data are ingested and maintained to a [PostgreSQL](https://www.postgresql.org/) database.
* **Movies** and **users** data are more or less stable, they are daily extracted with [Sqoop](https://sqoop.apache.org) and saved to a [Hive](https://hive.apache.org) table in the datalake.

* **Ratings** are extracted in real-time with a [Kafka](https://kafka.apache.org/). They are transformed with [Spark Streaming](https://spark.apache.org/streaming/) and saved in a [kudu](https://kudu.apache.org)-based Datamart.

##### Analysis
Ratings are used to daily updated a [Spark MLlib](https://spark.apache.org/mllib/) model that predicts user preferences. The recommender is based on collaborative filtering, it compares users' ratings and generates a similarity score. For each user the model recommends the preferences of the most similar users. I used a [Matrix Factorizetion model](https://spark.apache.org/docs/latest/mllib-collaborative-filtering.html) optimized with the Alternative Least Square method.

The model is exposed on a web application that allows the user to consult the ratings and rate films. The new added rating are used in real-time to update the model.

---

### DevOps principles and process automation

I automatized the development, deployment and monitoring of this project following the **7 DevOps Principles**. In the design I used only open source products in order to make it easy a portability to a different environment.

#### Configuration Management <img width="10%" style="float: right;" src="../images/ansible.png">
Automation of the provisioning of development and production instances. Instead of use configuration scripts or manually configure each instance, IT people knowlede is refined to a DSL-based software component that ensures the idempotency and convergency of the setup. I defined [Ansible](https://www.ansible.com/) [Playbooks](https://docs.ansible.com/ansible/latest/user_guide/playbooks.html) for each role in my cluster. This opens the possibility to configure new instances on-demand with the required role and services.
A playbook is easily understandable and versionable.


#### Infrastructure as a Code <img width="10%" style="float: right;" src="../images/terraform.png">
Also the cluster architecture can be defined as a software component. I defined each instance in Google Cloud Platform using [Terraform](https://www.terraform.io/) configuration files. This way is possible to scale the cluster on-demand. Terraform runs Ansible playbooks to provise each instance on creation.


#### Continuous Integration <img width="10%" style="float: right;" src="../images/github.png">
Each modification on the code is integrated in the final product at each commit. I hosted my code on Github and integrated it with a [Jenkins Blue Ocean](https://jenkins.io/projects/blueocean/) pipeline. This pipeline ensures the autonomous execution of a set of tests aand the deployment in production environment.


#### Continuous Testing <img width="10%" style="float: right;" src="../images/junit.png">
Each time the code is integrated to the centralized repository, a set of tests are autonomously runned. The execution of both feature and non-regression tests ensures the quality of the final product. The Jenkins pipeline deploys the code on a test environment that replicates the production one and run there all the test. if a test fails the pipiline is interrupted.


#### Continuous Delivery <img width="10%" style="float: right;" src="../images/jenking.png">
If all the tests work the software modification is merged in the release version, that is rebuild and it's ready for the deployment that happens only after an explicit command. The deployment is executed with Ansible in order to ensure a idempotent and convergent installation and the correct execution of the services.



#### Continuous Deployment <img width="10%" style="float: right;" src="../images/jenking.png">
If the trust in the pipeline is total each modification is directly deploied in production. This allows a continuous update of the final product so the team can focus on improve it.


#### Continuous Monitoring <img width="10%" style="float: right;" src="../images/grafana.png"> <img width="10%" style="float: right;" src="../images/prome.png"> <img width="10%" style="float: right;" src="../images/slack.png">
The whole development process and the product in production must be monitored in order to ensure the best possible quality. I used [Prometheus](https://prometheus.io/) to collect distributed metrics that are presented with a [Grafana](https://grafana.com/) dashboard. In case of alerts all the team is warned with a [Slack](https://slack.com/) bot


