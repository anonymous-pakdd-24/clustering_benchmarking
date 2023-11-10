# Benchmark generator

This is the repository of the benchmark generator proposed in the paper *AutoClues: Exploring Clustering Pipelines \\via AutoML and Diversification* submitted to PAKDD 2024.
To implement the optimization process, we departed from the code provided in [1] (GitHub repository: [https://github.com/aquemy/DPSO_experiments](https://github.com/aquemy/DPSO_experiments)).

[1] A. Quemy, "Data Pipeline Selection and Optimization." DOLAP. 2019. http://ceur-ws.org/Vol-2324/Paper19-AQuemy.pdf

# Requirements

In order to reproduce the experiments in any operating systems, Docker is required: [https://www.docker.com/](https://www.docker.com/).
Install it, and be sure that it is running when trying to reproduce the experiments.

To test if Docker is installed correctly:

- open the terminal;
- run ```docker run hello-world```.

***Expected output:***

```
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
2db29710123e: Pull complete
Digest: sha256:7d246653d0511db2a6b2e0436cfd0e52ac8c066000264b3ce63331ac66dca625
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```

# Reproducing the experiments

The instructions are valid for Unix-like systems (e.g., Linux Ubuntu, MacOS) and Windows (if using PowerShell).


Open the terminal and type:

```
docker run -it --volume ${PWD}/clustering_benchmarking:/home/clustering_benchmarking ghcr.io/anonymous-pakdd-24/clustering_benchmarking:1.0.0
```

This creates and mounts the folder ```autoclues``` into the container (which is populated with the code and the necessary scenarios), and run the toy example.


# Customize the experiments

You can modify the file ```resources/configspace.json``` to customize the search space.
