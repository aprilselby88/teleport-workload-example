from spiffe import WorkloadApiClient

# Fetch X.509 and JWT SVIDs
with WorkloadApiClient() as client:
    x509_svid = client.fetch_x509_svids()
    print(x509_svid)
    for svid in x509_svid:
        print(f'SPIFFE ID: {svid.spiffe_id}')
