import asyncio
from asyncua import Client
from asyncua.ua import UaStatusCodeError

async def main():
    url = "opc.tcp://127.0.0.1:4861"
    client = Client(url=url)
    
    print(f"Connexion au serveur OPC UA de WinCC Professional : {url}...")
    try:
        async with client:
            print(" Connexion réussie au Runtime WinCC !")
            
            # Try the direct tag name first
            node_path = "ns=1;s=t|DB_IIoTExport_GT_Drain_m3h"

            
            # Alternative paths if the above fails (uncomment if needed):
            # node_path = "ns=2;s=Variables IHM.DB_IIoTExport_GT_Drain_m3h"
            # node_path = "ns=2;s=Tags.DB_IIoTExport_GT_Drain_m3h"
            
            var_node = client.get_node(node_path)
            
            # Read the value
            valeur = await var_node.read_value()
            print(f"🎉 SUCCESS! Valeur lue dans WinCC pour {node_path} : {valeur}")
            
    except UaStatusCodeError as e:
        print(f"❌ Erreur OPC UA (Le chemin du nœud est probablement faux) : {e}")
    except Exception as e:
        print(f"❌ Autre erreur : {e}")

if __name__ == "__main__":
    asyncio.run(main())
