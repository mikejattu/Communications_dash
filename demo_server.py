from asyncua import Server, ua
import asyncio
from asyncua.server.users import User, UserRole
users_db = {
    "admin": "securepassword123",
    "operator": "operator123"
}

class UserManager:
    def get_user(self, iserver, username=None, password=None, certificate=None):
        if username in users_db and password == users_db[username]:
            return User(role=UserRole.User)
        return None

async def main():

    # Setup server
    server = Server(user_manager=UserManager())
    await server.init()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")
    
    # Setup security - enable username/password authentication
    server.set_security_policy([
        ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
        ua.SecurityPolicyType.Aes256Sha256RsaPss_SignAndEncrypt
    ])
    
    # Setup namespace
    uri = "http://examples.freeopcua.github.io"
    idx = await server.register_namespace(uri)
    
    # Create a new object node
    myobj = await server.nodes.objects.add_object(idx, "OilSandTank")
    
    # Add a variable node
    oil_sand_level = await myobj.add_variable(idx, "Oil Sand Level", 85.0)
    confidence = await myobj.add_variable(idx, "Confidence Level", 25.0)
    await confidence.set_writable()  # Allow clients to write to this variable
    await oil_sand_level.set_writable()  # Allow clients to write to this variable

    # Start server
    async with server:
        while True:
            await asyncio.sleep(1)
if __name__ == "__main__":
    print("Starting OPC UA server...")
    print("Password protection enabled.")
    asyncio.run(main())