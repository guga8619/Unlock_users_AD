import os
import ssl
from ldap3 import Connection,Server,Tls,ALL,SUBTREE
from ldap3.extend.microsoft.unlockAccount import ad_unlock_account
from dotenv import load_dotenv

SERVERAD=os.getenv("SERVERAD")
USERAD=os.getenv("USERAD")
PASSWORDAD=os.getenv("PASSWORDAD")
USERBASE=os.getenv("USERBASE")
DOMINIO=os.getenv("DOMINIO")

load_dotenv()
def unlockuser(user):
    USER_DN_FILTER = lambda u: f"(&(objectClass=user)(objectCategory=Person)(sAMAccountName={u}))"
    def query(USER_DN_FILTER):
        obj=con.extend.standard.paged_search(user_base,'(%s=%s)'%(id_name,f"{con.entries[0].sAMAccountName}@agea.com.ar"))
        result_set = []
        for entry in obj:
            if "dn" in entry:
                d = entry["attributes"]
                d["dn"] = entry["dn"]
                result_set.append(d)
        return result_set

    def unlockaccount():
        if len(con.entries) == 0:
            result="El usuario no fue encontrado"
            print(result)
            return result
        elif con.entries[0].UserAccountControl.value == 514:
            result="Usuario deshabilitado"
            print(result)
            return result
        else:
            lock=str(con.entries[0].lockoutTime.value)
            if lock.split("-")[0]== "1601" and con.entries[0].UserAccountControl.value != 514:
                result="El usuario no esta bloqueado"
                print(result) 
                return result
            else:
                resultquery=query(USER_DN_FILTER(""))
                try:
                    user=resultquery[0]
                    unlock = ad_unlock_account(con, user["dn"])
                    if isinstance(unlock, bool):
                        result="Usuario desbloqueado con exito"
                        print(result)
                        return result
                except:
                    result="Usuario con permisos especiales comunicarse con Mesa de ayuda de sistemas"
                    print(result) 
                    return result
    try:
        id_name="cn"
        t = Tls(validate=ssl.CERT_NONE)
        user_base=USERBASE
        server=Server(SERVERAD,use_ssl=True, tls=t,get_info=ALL)
        con = Connection(server,USERAD,PASSWORDAD,auto_bind=True)
        
        if con.bound:
            con.search(user_base,'(%s=%s)'%(id_name,user),search_scope=SUBTREE,attributes=['*'])
            if len(con.entries) == 0:
                id_name="userPrincipalName"
                con.search(user_base,'(%s=%s)'%(id_name,f"{user}{DOMINIO}"),search_scope=SUBTREE,attributes=['*'])
                if len(con.entries) == 0:
                    result="usuario no encontrado comunicarse con Mesa de ayuda de sistemas"
                    print(result)
                    return result
                else:
                    result=unlockaccount()
                    print(result)
                    return result
            else:
                result=unlockaccount()
                print(result)
                return result
    except Exception as e:
        print(e)

"""
LISTA DE ATRIBUTOS DISPONIBLES

['accountExpires', 'badPasswordTime',
'badPwdCount', 'cn', 'codePage', 'company', 'countryCode', 'dSCorePropagationData', 'department', 'description', 'displayName', 'distinguishedName',
'employeeID', 'employeeNumber', 'employeeType', 'extensionAttribute10', 'extensionAttribute11', 'extensionAttribute14', 'extensionAttribute15', 'extensionAttribute3', 
'extensionAttribute4', 'extensionAttribute5', 'extensionAttribute6', 'extensionAttribute7', 'extensionAttribute8', 'extensionAttribute9', 'givenName', 'homePhone',
'instanceType', 'l', 'lastLogoff', 'lastLogon', 'lastLogonTimestamp', 'legacyExchangeDN', 'lockoutTime', 'logonCount', 'logonHours', 'mail', 'mailNickname', 
'manager', 'memberOf', 'mobile', 'msExchBlockedSendersHash', 'msExchMailboxGuid', 'msExchMobileMailboxFlags', 'msExchPoliciesExcluded',
'msExchRecipientDisplayType', 'msExchRecipientTypeDetails', 'msExchRemoteRecipientType', 'msExchTextMessagingState', 'msExchUMDtmfMap',
'msExchUserAccountControl', 'msExchUserHoldPolicies', 'msExchVersion', 'msExchWhenMailboxCreated', 'name', 'objectCategory', 
'objectClass', 'objectGUID', 'objectSid', 'pager', 'primaryGroupID', 'protocolSettings', 'proxyAddresses', 'publicDelegatesBL',
'pwdLastSet', 'sAMAccountName', 'sAMAccountType', 'scriptPath', 'showInAddressBook', 'sn', 'targetAddress', 'telephoneNumber',
'textEncodedORAddress', 'title', 'uSNChanged', 'uSNCreated', 'userAccountControl', 'userPrincipalName', 'whenChanged', 'whenCreated']
"""

if __name__ == "__main__":
    print(unlockuser("nbarboza"))