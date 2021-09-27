
from pysnmp import hlapi
import datetime


def construct_object_types(list_of_oids):
    object_types = []
    for oid in list_of_oids:
        object_types.append(hlapi.ObjectType(hlapi.ObjectIdentity(oid)))
    return object_types


def cast(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        try:
            return float(value)
        except (ValueError, TypeError):
            try:
                return str(value)
            except (ValueError, TypeError):
                pass
    return value


def fetch(handler, count):
    result = []
    for i in range(count):
        try:
            error_indication, error_status, error_index, var_binds = next(handler)
            if not error_indication and not error_status:
                items = {}
                for var_bind in var_binds:
                    items[str(var_bind[0])] = cast(var_bind[1])
                result.append(items)
            else:
                raise RuntimeError('Got SNMP error: {0}'.format(error_indication))
        except StopIteration:
            break
    return result


def get(target, oids, credentials, port=161, engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
    handler = hlapi.getCmd(
        engine,
        credentials,
        hlapi.UdpTransportTarget((target, port)),
        context,
        *construct_object_types(oids)
    )
    return fetch(handler, 1)[0]


print(get('192.168.1.1', ['1.3.6.1.2.1.1.5.0'], hlapi.CommunityData('private_cisco')))  # system name (hostname)

# print(get('192.168.1.1', ['1.3.6.1.2.1.1.3.0'], hlapi.CommunityData('private_cisco')))  # outputs tick value
# ## system up time ##
uptime = get('192.168.1.1', ['1.3.6.1.2.1.1.3.0'], hlapi.CommunityData('private_cisco'))
seconds = uptime["1.3.6.1.2.1.1.3.0"]/100
print("{'1.3.6.1.2.1.1.3.0' :", datetime.timedelta(seconds=seconds.__round__()), "}")
# ####################

print(get('192.168.1.1', ['1.3.6.1.2.1.1.4.0'], hlapi.CommunityData('private_cisco')))  # system contact (cantact info)
print(get('192.168.1.1', ['1.3.6.1.2.1.1.6.0'], hlapi.CommunityData('private_cisco')))  # system location

# ## system info ##
sys_info = get('192.168.1.1', ['1.3.6.1.2.1.1.1.0'], hlapi.CommunityData('private_cisco'))
sys_info_v = sys_info["1.3.6.1.2.1.1.1.0"].split("M3")
print("{'1.3.6.1.2.1.1.1.0' :", sys_info_v[0], "}")
# #################


# ## sys tick to time ###
# uptime = get('192.168.1.1', ['1.3.6.1.2.1.1.3.0'], hlapi.CommunityData('private_cisco'))
# seconds = uptime["1.3.6.1.2.1.1.3.0"]/100
# print("time :", datetime.timedelta(seconds=seconds.__round__()), "timer")
# #######################

print("")
# snmp-server community cisco rw
