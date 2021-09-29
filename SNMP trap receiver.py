
from pysnmp.entity import engine, config
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv

snmpEngine = engine.SnmpEngine()

TrapAgentAddress = '192.168.1.2'  # Trap listener address (local pc)
Port = 162  # trap listener port


config.addTransport(
    snmpEngine,
    udp.domainName,  # + (1,),
    udp.UdpTransport().openServerMode((TrapAgentAddress, Port)))

# Configure community here
config.addV1System(snmpEngine, ' ', 'public_cisco')  # (snmpEngine, '?', 'community string')

print("Agent is listening SNMP Trap on " + TrapAgentAddress + " , Port : " + str(Port))
print('--------------------------------------------------------------------------')


# this function prints all received message from trap
def cb_fun(snmp_engine, state_reference, context_engine_id, context_name, var_binds, cb_ctx):
    print("Received new Trap message")
    for name, val in var_binds:
        print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))  # "'%s = %s' %" text formatting


ntfrcv.NotificationReceiver(snmpEngine, cb_fun)
# makes a simulate never-ending job for input and output
snmpEngine.transportDispatcher.jobStarted(1)  # 1 == job id

try:
    snmpEngine.transportDispatcher.runDispatcher()

except:
    snmpEngine.transportDispatcher.closeDispatcher()
    raise

