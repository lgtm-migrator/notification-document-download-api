import os
import sys
import traceback

workers = 4
worker_class = "eventlet"
worker_connections = 256
bind = "0.0.0.0:{}".format(os.getenv("PORT"))
accesslog = '-'

# See AWS doc
# > We also recommend that you configure the idle timeout of your application
# to be larger than the idle timeout configured for the load balancer.
# > By default, Elastic Load Balancing sets the idle timeout value for your load balancer to 60 seconds.
# https://docs.aws.amazon.com/elasticloadbalancing/latest/application/application-load-balancers.html#connection-idle-timeout
on_aws = os.environ.get("NOTIFY_ENVIRONMENT", "") in ["production", "staging"]
if on_aws:
    keepalive = 75


def on_starting(server):
    server.log.info("Starting Document Download API")


def worker_abort(worker):
    worker.log.info("worker received ABORT {}".format(worker.pid))
    for threadId, stack in sys._current_frames().items():
        worker.log.error(''.join(traceback.format_stack(stack)))


def on_exit(server):
    server.log.info("Stopping Document Download API")


def worker_int(worker):
    worker.log.info("worker: received SIGINT {}".format(worker.pid))
