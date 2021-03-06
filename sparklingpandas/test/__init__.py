"""
Tests for the PandaSpark module, you probably don't want to import this
directly.
"""
import subprocess as sub
import os
import logging


def run_cmd(cmd):
    """Execute the command and return the output if successful. If
    unsuccessful, print the failed command and its output.
    """
    try:
        out = sub.check_output(cmd, shell=True, stderr=sub.STDOUT)
        return out
    except sub.CalledProcessError, err:
        logging.error("The failed test setup command was [%s]." % err.cmd)
        logging.error("The output of the command was [%s]" % err.output)
        raise


CHECK_SPARK_HOME = """
if [ -z "$SPARK_HOME" ]; then
   echo "Error: SPARK_HOME is not set, can't run tests."
   exit -1
fi
"""
os.system(CHECK_SPARK_HOME)

# Dynamically load project root dir and sparkling pandas jars.
project_root = os.getcwd()
jars = run_cmd("ls %s/target/scala-2.10/*.jar" % project_root)

# Set environment variable that specifies we are running a test.
os.environ['IS_TEST'] = "True"

# Set environment variables.
os.environ["PYTHONPATH"] = project_root
os.environ["PYSPARK_SUBMIT_ARGS"] = ("--jars %s --driver-class-path %s" +
                                     " pyspark-shell") % (jars, jars)
os.environ["JARS"] = jars
os.environ["SPARK_CONF_DIR"] = "%s/sparklingpandas/test/resources/conf" % \
                               project_root
