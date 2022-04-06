#! /bin/bash
if [ "$ARQ_RELOAD" = "1" ]
then
  arq --watch . arq_queue.config.WorkerSettings
else
  arq arq_queue.config.WorkerSettings
fi
exec "$@"