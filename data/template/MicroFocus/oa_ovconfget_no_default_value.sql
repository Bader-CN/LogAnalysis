SELECT * FROM oa_config
WHERE id NOT IN (SELECT id FROM oa_config WHERE
(key == '[agent.health].OPC_HB_MSG_INTERVAL' AND VALUE == '1800') OR
(key == '[agent.health].OPC_SELFMON_ENABLE' AND VALUE == 'true') OR
(key == '[agtrep].ACTION_TIMEOUT' AND VALUE == '3') OR
(key == '[agtrep].INSTANCE_DELETION_THRESHOLD' AND VALUE == '5') OR
(key == '[bbc.cb].LOCAL_CONTROL_ONLY' AND VALUE == 'true') OR
(key == '[bbc.cb].LOCAL_INFO_ONLY' AND value == 'true') OR
(key == '[bbc.cb].REQUEST_TIMEOUT' AND value == '1') OR
(key == '[bbc.cb].RESTRICT_REG' AND value == 'true') OR
(key == '[bbc.cb].SSL_REQUIRED' AND value == 'true') OR
(key == '[bbc.fx].FX_MAX_RETRIES' AND value == '3') OR
(key == '[bbc.http].LOCAL_INFO_ONLY' AND value == 'false') OR
(key == '[bbc.http].LOG_SERVER_ACCESS' AND value == 'false') OR
(key == '[bbc.http].MAX_CONNECTIONS' AND value == '0') OR
(key == '[bbc.http].SERVER_PORT' AND value == '0') OR
(key == '[bbc.http.ext.opcmsga].AUTO_CONNECTION_CLOSE_INTERVAL' AND value == '60') OR
(key == '[bbc.snf].MAX_FILE_BUFFER_SIZE' AND value == '0') OR
(key == '[coda].DATAMATRIX_ROWCOUNT' AND value == '5') OR
(key == '[coda].DATAMATRIX_VERSION' AND value == '1') OR
(key == '[coda].EXTRACT_RESTRICT_SYMLINK' AND value == 'false') OR
(key == '[coda].SSL_SECURITY' AND value == 'NONE') OR
(key == '[coda.comm].LOG_SERVER_ACCESS' AND value == 'false') OR
(key == '[coda.comm].SERVER_BIND_ADDR' AND value == 'localhost') OR
(key == '[coda.comm].SERVER_PORT' AND value == '0') OR
(key == '[conf.cluster.RGState.HACMP].ACQUIRING' AND value == 'offline') OR
(key == '[conf.cluster.RGState.HACMP].ERROR' AND value == 'unknown') OR
(key == '[conf.cluster.RGState.HACMP].ERROR_SECONDARY' AND value == 'unknown') OR
(key == '[conf.cluster.RGState.HACMP].OFFLINE' AND value == 'offline') OR
(key == '[conf.cluster.RGState.HACMP].OFFLINE_SECONDARY' AND value == 'offline') OR
(key == '[conf.cluster.RGState.HACMP].ONLINE' AND value == 'online') OR
(key == '[conf.cluster.RGState.HACMP].ONLINE_SECONDARY' AND value == 'online') OR
(key == '[conf.cluster.RGState.HACMP].RELEASING' AND value == 'offline') OR
(key == '[conf.cluster.RGState.HACMP].UNKNOWN' AND value == 'unknown') OR
(key == '[conf.cluster.RGState.HACMP].UNMANAGED_SECONDARY' AND value == 'unknown') OR
(key == '[conf.cluster.RGState.MCSG].down' AND value == 'offline') OR
(key == '[conf.cluster.RGState.MCSG].halting' AND value == 'unknown') OR
(key == '[conf.cluster.RGState.MCSG].starting' AND value == 'unknown') OR
(key == '[conf.cluster.RGState.MCSG].unknown' AND value == 'unknown') OR
(key == '[conf.cluster.RGState.MCSG].up' AND value == 'online') OR
(key == '[conf.cluster.RGState.MSCS].ClusterGroupFailed' AND value == 'offline') OR
(key == '[conf.cluster.RGState.MSCS].ClusterGroupOffline' AND value == 'offline') OR
(key == '[conf.cluster.RGState.MSCS].ClusterGroupOnline' AND value == 'online') OR
(key == '[conf.cluster.RGState.MSCS].ClusterGroupPartialOnline' AND value == 'offline') OR
(key == '[conf.cluster.RGState.MSCS].ClusterGroupStateUnknown' AND value == 'unknown') OR
(key == '[conf.cluster.RGState.RHAS].started' AND value == 'online') OR
(key == '[conf.cluster.RGState.SC].ERROR_STOP_FAILED' AND value == 'unknown') OR
(key == '[conf.cluster.RGState.SC].OFFLINE' AND value == 'offline') OR
(key == '[conf.cluster.RGState.SC].ONLINE' AND value == 'online') OR
(key == '[conf.cluster.RGState.SC].PENDING_OFFLINE' AND value == 'unknown') OR
(key == '[conf.cluster.RGState.SC].PENDING_ONLINE' AND value == 'unknown') OR
(key == '[conf.cluster.RGState.SC].UNMANAGED' AND value == 'unknown') OR
(key == '[conf.cluster.RGState.SLEHA].running' AND value == 'online') OR
(key == '[conf.cluster.RGState.VCS].OFFLINE' AND value == 'offline') OR
(key == '[conf.cluster.RGState.VCS].ONLINE' AND value == 'online') OR
(key == '[conf.cluster.RGState.VCS]._OFFLINE_' AND value == 'offline') OR
(key == '[conf.cluster.RGState.VCS]._ONLINE_' AND value == 'online') OR
(key == '[conf.cluster.RGState.VCS]._PARTIAL_' AND value == 'unknown') OR
(key == '[conf.cluster.RGState.VCS]._UNKNOWN_' AND value == 'unknown') OR
(key == '[conf.core].ASYNC_CONTROL_NOTIFY' AND value == 'false') OR
(key == '[conf.core].CACHE_CONFIGSETTINGS_POLICIES' AND value == 'true') OR
(key == '[conf.core].FORMAT_POLICY_LIST' AND value == 'false') OR
(key == '[conf.core].MERGED_POLICY_LIST_FILENAME' AND value == 'ov_policies.txt') OR
(key == '[conf.server].AUDIT_LOGGING' AND value == 'false') OR
(key == '[conf.server].AUDIT_LOG_MODE' AND value == 'ALL') OR
(key == '[conf.server].LOCATE_SERVER' AND value == '5') OR
(key == '[conf.server].NOMULTIPLEPOLICIES' AND value == 'mgrconf,msgforwarding,servermsi,ras') OR
(key == '[conf.server].PING_SERVER' AND value == '15') OR
(key == '[conf.server].WAIT_TIME' AND value == '3') OR
(key == '[ctrl].RUN_PROFILE' AND value == 'false') OR
(key == '[ctrl].START_ON_BOOT' AND value == 'false') OR
(key == '[ctrl.ovcd].ACTION_TIMEOUT' AND value == '60') OR
(key == '[ctrl.ovcd].KILL_TIMEOUT' AND value == '15') OR
(key == '[ctrl.ovcd].MONITOR_CHECK_INTERVAL' AND value == '2000') OR
(key == '[ctrl.ovcd].PROCESS_TIMEOUT' AND value == '120') OR
(key == '[ctrl.ovcd].STOP_ALERT_WAIT_INTERVAL' AND value == '30') OR
(key == '[ctrl.sudo].OV_SUDO' AND value == '""') OR
(key == '[depl].CMD_TIMEOUT' AND value == '600000') OR
(key == '[depl].DEPLOY_MECHANISMS' AND value == 'ssh') OR
(key == '[depl.bootstrap].BUNDLE_NAME' AND value == 'OVO-Client') OR
(key == '[depl.bootstrap].BUNDLE_VERSION' AND value == 'A.08.10.160') OR
(key == '[depl.mechanisms.ssh].COPY' AND value == 'pscp -q  -batch -pw <passwd> <sourcefile> <user>@<host>:<targetfile>') OR
(key == '[depl.mechanisms.ssh].EXEC' AND value == 'plink -ssh -batch -2 -pw <passwd> <user>@<host> <command>') OR
(key == '[eaagt].DISABLEPERF' AND value == 'FALSE') OR
(key == '[eaagt].OPC_MONA_CONF_RPC_ONLY' AND value == 'FALSE') OR
(key == '[eaagt].OPC_PUB_DIR_NOT_WW' AND value == 'TRUE') OR
(key == '[eaagt].OPC_RPC_ONLY' AND value == 'TRUE') OR
(key == '[eaagt].OPC_SEND_ASSD_ON_DEPLOYMENT' AND value == 'ON_DEVIATION') OR
(key == '[hpcsrvd].ENFORCE_SERVER_SSL' AND value == 'REMOTE') OR
(key == '[hpsensor].ENFORCE_SERVER_SSL' AND value == 'ALL') OR
(key == '[oacore].ENABLE_BASELINE' AND value == 'false') OR
(key == '[oacore].UPDATED_MODEL_AVAILABLE' AND value == 'TRUE') OR
(key == '[oacore.dml].READ_ONLY_MODE' AND value == 'false') OR
(key == '[oacore.sqlite].RELEASE_MEMORY' AND value == 'true') OR
(key == '[sec.cm].ASYMMETRIC_KEY_LENGTH' AND value == '2048') OR
(key == '[sec.cm.certificates].CERTIFICATE_AUTORENEW' AND value == 'TRUE') OR
(key == '[sec.cm.certificates].CERTIFICATE_RENEWAL_CHECK_PERIOD' AND value == '10') OR
(key == '[sec.cm.certificates].CERT_RENEW_ALERT_MSG_LOG_ONLY' AND value == 'TRUE') OR
(key == '[sec.cm.certificates].CERT_RENEW_REQ_STATUS' AND value == 'NOT_SENT') OR
(key == '[sec.core].DEF_SYM_KEY_ALGO' AND value == 'eAES128') OR
(key == '[sec.core].ENABLE_DEF_SYM_KEY_ALGO' AND value == 'TRUE') OR
(key == '[sec.core].SIGNATURE_HASH_ALGO' AND value == 'eSHA256') OR
(key == '[sec.core.auth.mapping.actionallow].conf' AND value == '80') OR
(key == '[sec.core.auth.mapping.actionallow].ctrl' AND value == '4') OR
(key == '[sec.core.auth.mapping.actionallow].depl' AND value == '1280') OR
(key == '[sec.core.auth.mapping.actionallow].eaagt.actr' AND value == '1') OR
(key == '[sec.core.auth.mapping.manager].conf' AND value == '511') OR
(key == '[sec.core.auth.mapping.manager].ctrl' AND value == '15') OR
(key == '[sec.core.auth.mapping.manager].depl' AND value == '2047') OR
(key == '[sec.core.auth.mapping.manager].eaagt.actr' AND value == '1') OR
(key == '[sec.core.auth.mapping.secondary].conf' AND value == '511') OR
(key == '[sec.core.auth.mapping.secondary].ctrl' AND value == '15') OR
(key == '[sec.core.auth.mapping.secondary].depl' AND value == '2047') OR
(key == '[sec.core.auth.mapping.secondary].eaagt.actr' AND value == '1') OR
(key == '[sec.core.ssl].COMM_PROTOCOL' AND value == 'TLSv1.2') OR
(key == '[xpl.log].addlocales' AND value == 'none') OR
(key == '[xpl.log].apSpecifcUseParent' AND value == 'true') OR
(key == '[xpl.log].handlers' AND value == 'none') OR
(key == '[xpl.log].logparent' AND value == 'false') OR
(key == '[xpl.log.OvLogFileHandler].filecount' AND value == '10') OR
(key == '[xpl.log.OvLogFileHandler].filesize' AND value == '1') OR
(key == '[xpl.net].DISABLE_EXT_ENTITIES' AND value == 'TRUE') OR
(key == '[xpl.net].SOCKETS_PER_SOCKETSET' AND value == '10') OR
(key == '[xpl.net].SocketPoll' AND value == 'TRUE') OR
(key == '[xpl.trc.server].IsBindAny' AND value == 'YES'));