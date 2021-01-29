#!/bin/bash

if [ "$SLURM_JOBID" == "" ];then
  echo "RUNNING OUTSIDE OF SLURM CONTEXT"
  exit;
fi

export PATH=$(pwd)/sbin/bin:$PATH

export JAVA_HOME="/share/apps/jdk/1.8.0_271"
PATH=$JAVA_HOME/bin:$PATH
export PATH
echo $(java -version)
echo $(which java)

export SPARK_HOME="$(pwd)/sbin"

function _exists_()
{
    command -v "$1" >/dev/null 2>&1
}

# python3 or still python2 ?
if _exists_ python3; then
    export PYSPARK_PYTHON=$(which python3)
else
    export PYSPARK_PYTHON=$(which python)
fi

_conf_dir=${SLURM_SUBMIT_DIR}/sbin/conf
_logs_dir=${SLURM_SUBMIT_DIR}/sbin/logs
_work_dir=${SLURM_SUBMIT_DIR}

mkdir -p ${_conf_dir} ${_logs_dir}

export SPARK_CONF_DIR=${_conf_dir}
export SPARK_PID_DIR=${SLURM_JOB_TMP}

_master_node="$(hostname -s)-ib0"
_port=$(shuf -i 10000-65534 -n 1)
_memory=2G

function _setup_memory_()
{
    if [ "$SLURM_JOBID" != "" ]; then
        local memory_file="/sys/fs/cgroup/memory/slurm/uid_$UID/job_${SLURM_JOBID}/memory.limit_in_bytes"
        if [ -e $memory_file ]; then
            local mem=$(cat $memory_file)
            _memory="$(echo $mem/1024^3 | bc)G"
        fi
    fi
}

function _setup_spark_env_()
{
    cat<<EOF > ${_conf_dir}/spark-env.sh

export SPARK_MASTER_HOST=${_master_node}
export SPARK_MASTER_PORT=${_port}
export SPARK_WORKER_PORT=${_port}

export SPARK_LOCAL_IP=\$(hostname -s)-ib0
export SPARK_MASTER_IP=${_master_node}
export SPARK_WORKER_MEMORY=${_memory}
export SPARK_WORKER_CORES=${SLURM_CPUS_PER_TASK}
export SPARK_DAEMON_MEMORY=${_memory}
export SPARK_EXECUTOR_MEMORY=${_memory}

export SPARK_CONF_DIR=${_conf_dir}
export SPARK_LOG_DIR=${_logs_dir}

export SPARK_WORKER_DIR=${_work_dir}
export SPARK_PID_DIR=${SLURM_JOB_TMP}

export JAVA_HOME=${JAVA_HOME}

export PATH=$PATH

export PYTHONPATH=$PYTHONPATH

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH

EOF

    export MEMORY=${_memory}

}

function _setup_slaves_()
{
    (
        local node=
        for node in $(scontrol show hostname $SLURM_NODELIST); do
            echo "${node}-ib0"
        done
    ) > ${_conf_dir}/slaves
}

function _setup_spark_defaults_conf_()
{
    cat<<EOF > ${_conf_dir}/spark-defaults.conf

spark.executorEnv.JAVA_HOME ${JAVA_HOME}

EOF

}

function start_all()
{
    _setup_memory_
    _setup_spark_env_
    _setup_slaves_
    _setup_spark_defaults_conf_

    export SPARK_URL="spark://${_master_node}:${_port}"

    echo "-------------------start spark"
    ${SPARK_HOME}/sbin/start-all.sh
}

function stop_all()
{
    ${SPARK_HOME}/sbin/stop-all.sh
}
