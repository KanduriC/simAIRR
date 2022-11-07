FROM ubuntu:20.04

COPY . simAIRR
RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install python3.8 python3-pip git-all -y
RUN pip3 install ./simAIRR