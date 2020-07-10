Scanning Handle Records
=======================

Each dataset handle record is checked as follows:

1. Is the the dataset still current (we are restricting attention to datasets published before April -- so many will have been replaced)?
2. Do all the files in the dataset conform to the dataset id (e.g. same experiment, same table)?
3. Is the master version older than the replicas (indicates some publication irregularity)?

Additional checks have been run on availability of masks, where masks are needed (_the search for masks is currently very light, so results are worse than they should be__


Results are summarised in a `json` file, which contains two top level entries, `header` and `results`. The `results` section contains a dictionary for each handle, such as the following 
two:

```
        "hdl:21.14100/000cce7f-69c7-333f-8c46-07825bc73cf3": {
            "dset_id": "CMIP6.CMIP.CAS.FGOALS-f3-L.piControl.r1i1p1f1.Omon.thetao.gn.v20191028",
            "error_level": 2,
            "qc_message": "mask_error",
            "qc_status": "ERROR"
        },
        "hdl:21.14100/001413f5-1913-3b13-942c-cbf9175c8eb7": {
            "dset_id": "CMIP6.ScenarioMIP.CCCma.CanESM5.ssp126.r1i1p1f1.AERmon.od550aer.gn.v20190429",
            "error_level": 0,
            "qc_status": "pass"
        },
```

The `qc_message` is not very informative at present .. more detail will be added when the errors are better understood.

