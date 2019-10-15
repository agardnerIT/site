---
layout: post
title: Kubernetes Cluster on AWS
categories: [kubernetes, aws]
---

Create a single node Kubernetes cluster, fully integrated with AWS (automatic Load Balancers for frontend services) for testing purposes…

## Prerequisites

- An AWS account.
- An SSH Keypair created in AWS and have the PEM file stored locally.
- Your AWS Access Key & Secret Key

> Following this tutorial will incur AWS costs.

## Install Kubectl

`kubectl` (kubernetes control) is the command line utility you will use to interact with your Kubernetes cluster once it’s up & running.

Depending on your operating system, installation will obviously be different but the official instructions here are a great place to start.

Before you proceed, ensure you can successfully run the command `kubectl version` in your command line.

Note: You might see this warning. It’s safe to ignore.

> The connection to the server localhost:8080 was refused - did you specify the right host or port?

## Generate Public Key From PEM

Ensure your pem has `0600` permissions: `chmod 0600 key.pem`

Generate the public key from your private key PEM file:

{% raw %}
```
ssh-keygen -y -f key.pem > key.pub
```
{% endraw %}

## Install EKSCTL Utility

`eksctl` (Amazon Elastic Kubernetes Service Control) is a command line utility which makes it easy to interact with the AWS EKS service.

Installing `eksctl` is very easy, depending on your OS:

## Standard Linux Install

{% raw %}
```
curl --silent --location "https://github.com/weaveworks/eksctl/releases/download/latest_release/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin
```
{% endraw %}

## MacOS Install Using Homebrew

{% raw %}
```
brew tap weaveworks/tap
brew install weaveworks/tap/eksctl
```
{% endraw %}

## Windows Install Using Chocolatey

{% raw %}
```
chocolatey install eksctl
```
{% endraw %}

Before proceeding, ensure you can successfully run `eksctl version` in a command line.

## Authenticating EKSCTL

Since `eksctl` will be interacting with AWS on our behalf, we need to ensure it has permissions to authenticate.

Ensure you have the following folder structure & file created. If you’ve previously used any other tool that interacts with AWS (kops, Terraform etc) then chances are you’ll be good to go & won’t need to recreate anything.

Make sure the `~/.aws` folder exists and create a file called `credentials` inside. Edit the `credentials` file to include your AWS Access Key and AWS Secret Key.

Your credentials file should look like this:

{% raw %}
```
[default]
aws_access_key_id=AKIA***********
aws_secret_access_key=oRsRbKc*********
```
{% endraw %}

## Cluster Definition File

Create a cluster definition file. `eksctl` will use this file to define exactly how we want our cluster to be created. The file can be called anything (as long as it’s saved with the `.yaml` extension).

I’ll call mine `clusterDef.yaml` and store it in my home directory `~/clusterDef.yaml`

> Note on YAML: YAML does not work with tabs. Use space characters only.<br />Use [YAMLLint](http://www.yamllint.com) to validate your YAML file format.

{% raw %}
```
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig

metadata:
  name: single-node-cluster
  region: us-east-2

nodeGroups:
  - name: node-group-1
    instanceType: t2.medium
    desiredCapacity: 1
    ssh:
      publicKeyPath: /path/to/key.pub
```
{% endraw %}

Hopefully this should be fairly self explanatory. We create a cluster called `single-node-cluster` in the `us-east-2` region which consists of a single node (`desiredCapacity: 1`) which is a `t2.medium` sized node. We also copy our public key onto the instance so that we can SSH into the node if needed (although that shouldn’t be required).

## Create Cluster

All that’s left now is to actually create the cluster. `eksctl` makes this easy:

{% raw %}
```
eksctl create cluster -f ~/clusterDef.yaml
```
{% endraw %}
<br />
{% raw %}
```
$ eksctl create cluster -f /path/to/clusterDef.yaml
[i]  using region us-east-1
[i]  setting availability zones to [us-east-1b us-east-1c]
[i]  subnets for us-east-1b - public:192.168.0.0/19 private:192.168.64.0/19
[i]  subnets for us-east-1c - public:192.168.32.0/19 private:192.168.96.0/19
[i]  nodegroup "node-group-1" will use "ami-0f2e8e5663e16b436" [AmazonLinux2/1.13]
[i]  using SSH public key "/path/to/file.pub" as "eksctl-single-node-cluster-nodegroup-node-group-1-6f:84:05:83:7e:99:89:67:69:a6:7d:72:d7:0a:a4:c7" 
[i]  using Kubernetes version 1.13
[i]  creating EKS cluster "single-node-cluster" in "us-east-1" region
[i]  1 nodegroup (node-group-1) was included
[i]  will create a CloudFormation stack for cluster itself and 1 nodegroup stack(s)
[i]  if you encounter any issues, check CloudFormation console or try 'eksctl utils describe-stacks --region=us-east-1 --name=single-node-cluster'
[i]  2 sequential tasks: { create cluster control plane "single-node-cluster", create nodegroup "node-group-1" }
[i]  building cluster stack "eksctl-single-node-cluster-cluster"
[i]  deploying stack "eksctl-single-node-cluster-cluster"
[i]  building nodegroup stack "eksctl-single-node-cluster-nodegroup-node-group-1"
[i]  --nodes-min=1 was set automatically for nodegroup node-group-1
[i]  --nodes-max=1 was set automatically for nodegroup node-group-1
[i]  deploying stack "eksctl-single-node-cluster-nodegroup-node-group-1"
[✔]  all EKS cluster resource for "single-node-cluster" had been created
[✔]  saved kubeconfig as "/.../.kube/config"
[i]  adding role "arn:aws:iam::782430655514:role/eksctl-single-node-cluster-nodegr-NodeInstanceRole-DJGENWOS1P4E" to auth ConfigMap
[i]  nodegroup "node-group-1" has 0 node(s)
[i]  waiting for at least 1 node(s) to become ready in "node-group-1"
[i]  nodegroup "node-group-1" has 1 node(s)
[i]  node "ip-192-168-10-142.ec2.internal" is ready
[i]  kubectl command should work with "/.../.kube/config", try 'kubectl get nodes'
[✔]  EKS cluster "single-node-cluster" in "us-east-1" region is ready
```
{% endraw %}

## Delete Cluster

When you’re finished, delete the cluster with this command:

{% raw %}
```
eksctl delete cluster -f ~/clusterDef.yaml
```
{% endraw %}

*Deleting the cluster will not delete any resources that weren’t defined in the `clusterDef` file. In addition, deleting the cluster in this manner is still a bit buggy. Always double check that everything has actually been deleted to ensure you aren’t getting charged for leftover resources.*

{% raw %}
```
$ eksctl delete cluster -f ~/Documents/k8s/clusterDef.yaml 
[i]  using region us-east-1
[i]  deleting EKS cluster "single-node-cluster"
[✔]  kubeconfig has been updated
[i]  cleaning up LoadBalancer services
[i]  2 sequential tasks: { delete nodegroup "node-group-1", delete cluster control plane "single-node-cluster" [async] }
[i]  will delete stack "eksctl-single-node-cluster-nodegroup-node-group-1"
[i]  waiting for stack "eksctl-single-node-cluster-nodegroup-node-group-1" to get deleted
[i]  will delete stack "eksctl-single-node-cluster-cluster"
[✔]  all cluster resources were deleted
```
{% endraw %}

## Summary

This post gives you a quick and easy way to spin up an on-demand Kubernetes cluster in AWS for test / demo purposes.