import logging

# logging.
log = logging.getLogger()
print(log.getEffectiveLevel())  # warning 30
log.setLevel(logging.INFO)  # 默认格式是Warning
print(log.getEffectiveLevel())  # info 20
# logging.log(logging.log(), "debuglog")
logging.debug("debug")
logging.info("info")
logging.warning("warning")
logging.error("error")
logging.critical("critical")
