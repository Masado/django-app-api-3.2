# pull official base image
FROM ubuntu:latest

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV DEBIAN_FRONTEND=noninteractive

# install python and apt dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      apt-utils \
      bash \
      python3.8 \
      python3-pip \
      python3-setuptools \
      python3-dev \
      python-is-python3 \
      netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# install additional dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      ed \
	  less \
	  locales \
	  vim-tiny \
	  wget \
	  ca-certificates \
	  apt-transport-https \
	  gsfonts \
	  gnupg2 \
	  zip \
	  unzip \
	  tar \
	  texlive-latex-base texlive-fonts-recommended texlive-fonts-extra texlive-latex-extra \
	  docker \
	  curl \
	  git \
	  perl \
	  default-jre \
      libgfortran4 \
      build-essential \
      libssl-dev \
      uuid-dev \
      libgpgme11-dev \
      squashfs-tools \
      libseccomp-dev \
      pkg-config \
      gawk \
      gzip \
      rsync \
    && rm -rf /var/lib/apt/lists/*

# install psycopg2 dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      postgresql \
      gcc \
      musl \
    && rm -rf /var/lib/apt/lists/*
##############################
## install conda
# add conda bin to PATH
ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"

RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh
RUN conda --version
##############################
## install nextflow
RUN curl -s https://get.nextflow.io | bash \
    && mv nextflow /usr/local/bin \
    && nextflow info
##############################
## install r-base
# configure default locale
RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen \
	&& locale-gen en_US.utf8 \
	&& /usr/sbin/update-locale LANG=en_US.UTF-8

RUN echo "deb https://cloud.r-project.org/bin/linux/ubuntu focal-cran40/" > /etc/apt/sources.list.d/cran.list

# note proxy for gpg
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9

# set r-base version
ENV R_BASE_VERSION 4.1.0

## r-base
# install R and littler and set default CRAN repository
RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		littler\
		r-cran-littler \
		r-base \
        r-base-core \
		r-base-dev \
		r-recommended \
    && echo 'options(repos = c(CRAN = "https://cloud.r-project.org/"), download.file.method = "libcurl")' >> /etc/R/Rprofile.site \
    && echo 'source("/etc/R/Rprofile.site")' >> /etc/littler.r \
	&& ln -s /usr/share/doc/littler/examples/install.r /usr/local/bin/install.r \
	&& ln -s /usr/share/doc/littler/examples/install2.r /usr/local/bin/install2.r \
	&& ln -s /usr/share/doc/littler/examples/installGithub.r /usr/local/bin/installGithub.r \
	&& ln -s /usr/share/doc/littler/examples/testInstalled.r /usr/local/bin/testInstalled.r \
	&& install.r docopt \
	&& rm -rf /tmp/downloaded_packages/ /tmp/*.rds \
	&& rm -rf /var/lib/apt/lists/*

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		libcurl4-openssl-dev \
		libssl-dev \
		libxml2 \
		libxml2-dev \
    && rm -rf /var/lib/apt/lists/*

# check R version (should be 4.1.0)
RUN Rscript --version

##############################

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

