import unittest
from typing import List

from cass_graph_client.cass_graph import CassGraph
from cass_graph_client.test.resources.utils import load_or_instantiate


class RecommenderTest(unittest.TestCase):
    # <editor-fold desc="Test Setup">

    competencies = {
        "Macro 1.": "c4ac4737-c404-4906-b8fe-a85f557e08e3",
            "Competency 1.1": "42305968-0bf3-4858-8e1f-3529154f3a2e",
                "Micro 1.1.1": "e4f8021b-8973-4c79-9081-140a4d57ba77",
                    "1.1.1.A": "32a8496c-1bb7-4e28-9eb5-17ffad416caa",
                        "1.1.1.A.1": "0721c247-b6a5-49a0-a465-778e6e5da6a6",
                        "1.1.1.A.2": "78d38421-3692-498f-bc8e-3749b0fa5ca3",
                    "1.1.1.B": "7eb13891-bba5-4bfb-8937-a3fa68ced18a",
                        "1.1.1.B.1": "4cc020dd-7968-4e86-89fe-d747daf8d331",
                    "1.1.1.C": "772d5d4f-a42d-4847-a274-018e0ee1da4e",
                        "1.1.1.C.1": "60903f74-ca50-482b-8118-8d2ffb6459e2",
                "Micro 1.1.2": "47b46a13-7454-47fc-8317-8617e0c1df27",
                    "1.1.2.A": "18807aef-f3e7-4792-878f-c17308e0b31c",
                        "1.1.2.A.1": "a216681a-d18c-44ff-af7b-c771535b1b31",
                        "1.1.2.A.2": "ded0db99-d2a8-4975-a974-a299f59a3c6a",
                    "1.1.2.B": "d0bba337-4782-4479-8bed-cd4bd2c49cc2",
                        "1.1.2.B.1": "5853d307-b40d-443c-96d3-5b294f5d36e9",
                        "1.1.2.B.2": "700a3a54-87f2-4495-a6f5-33a7c9ec12b2",
                        "1.1.2.B.3": "c8934b45-61ea-4c85-b101-48d9e9b131e9",
                    "1.1.2.C": "1caa313c-440f-4fab-8a7e-24c0471b4edd",
                        "1.1.2.C.1": "de8d2391-8a7d-4cac-b2a5-043efa361b0f",
                        "1.1.2.C.2": "504154a0-2fd3-479c-8208-93ad1c3c876a",
                "Micro 1.1.3": "e92ae027-64c8-44bb-9333-5d2d8443529a",
                    "1.1.3.A": "5a5b756b-d39b-42fe-bd96-cfac76dbe403",
                        "1.1.3.A.1": "563e5ceb-efad-4e0c-bef4-87557f07bfc9",
                        "1.1.3.A.2": "96a664f7-7413-4807-9cf2-aabfbc205a9d",
                    "1.1.3.B": "268b9ba9-1979-4342-bfaa-54eb41a42064",
                        "1.1.3.B.1": "915e6614-5246-4d73-bf91-41ebaa9d49ec",
                        "1.1.3.B.2": "074ee029-da57-4125-b97b-8a71e64f2f2e",
                        "1.1.3.B.3": "429532eb-690f-4905-8c66-fd1a084a70b4",
                    "1.1.3.C": "085c8e65-64f9-4ebc-8b55-34a527e0ff93",
                        "1.1.3.C.1": "c0df9e81-5dcb-4cff-8925-ab3ec87e13dc",
                        "1.1.3.C.2": "acf2d6f4-e49d-416d-bdea-80b5b9888ee8",
            "Competency 1.2": "0bad5fb1-3ce0-472a-a49f-eb73add39c15",
                "Micro 1.2.1": "cf337efb-3350-4064-8f1b-232666585730",
                    "1.2.1.A": "3852e22c-3714-4a6d-b14a-ba4b57f8090e",
                        "1.2.1.A.1": "9d091407-a485-4ed4-9bd6-c6f64d2fe474",
                        "1.2.1.A.2": "e951f452-8ecf-479a-b3f1-21f137900d89",
                    "1.2.1.B": "ddd6a4e5-da13-4dab-92ed-1f150a55e9df",
                        "1.2.1.B.1": "5abe167a-ef1e-422e-ba29-292297a7667b",
                        "1.2.1.B.2": "7f2909a9-bd08-4041-bcd8-068a5792c391",
                        "1.2.1.B.3": "d78a889e-f631-4fb7-9734-bc13b2a548c3",
                        "1.2.1.B.4": "86b62333-0395-4a88-917b-c5e40212aa6a",
                    "1.2.1.C": "2ddfadfa-19f9-47e6-a56f-b28ef6b24d8e",
                "Micro 1.2.2": "fc459c33-1f0d-432c-bada-3622a178d193",
                    "1.2.2.A": "e618a0dd-94b7-4f33-8808-4a629ec92186",
                        "1.2.2.A.1": "a4fd9587-748f-4f41-a595-53393074cb43",
                    "1.2.2.B": "5757cd73-c02f-46d9-bd02-e8fa31dd219e",
                        "1.2.2.B.1": "cdbe40f0-5416-4357-bf65-c8e0324ee826",
                        "1.2.2.B.2": "28b82e2e-f2fd-4d99-b282-d5cb4c203c95",
                        "1.2.2.B.3": "a9c8426b-21b6-4645-8885-a0b1fa58785c",
                    "1.2.2.C": "37bb6a5a-b726-493a-b5df-bcc11f59cb38",
                "Micro 1.2.3": "d3a0b781-dc98-4ad4-8b3f-e3a56a64cad9",
                    "1.2.3.A": "d3ed27e4-c6ed-43a5-81aa-5f957283da8e",
                        "1.2.3.A.2": "8188f710-06a4-402e-a295-b63fa74cefc9",
                        "1.2.3.A.3": "b044537c-280f-4d58-ae7f-8ece6f2d7ee7",
                    "1.2.3.B": "72fe7e44-2d15-4973-b8e1-1b6b48767498",
                        "1.2.3.B.1": "61087252-f7d4-430b-920a-e828b17f3fb2",
                        "1.2.3.B.2": "a51d2002-4e45-4238-9a6e-4148422dc87f",
                        "1.2.3.B.3": "02208c9a-5471-4c44-bc06-bdc64f25aa49",
                    "1.2.3.C": "d24538a4-10be-4f8f-821e-937a91d1d85f",
                        "1.2.3.C.1": "ac49555b-b3d9-4fdd-925a-48a784df57c1",
                        "1.2.3.C.2": "3a37aeeb-8acb-494f-92e6-f7ce31be8671",
                        "1.2.3.C.3": "c856ff9c-c4a3-47b4-987c-ad0f5d07a7ff",
                "Micro 1.2.4": "e9325c31-3fa1-4462-8f61-d6b79daa31c4",
                    "1.2.4.A": "d7c98e01-fe5d-4259-ab6f-0a4b45c522ea",
                        "1.2.4.A.1": "b718d9b9-41ec-4f07-b767-674ba2fecc47",
                        "1.2.4.A.2": "c196d3f8-4c26-453e-b3f1-838afdfd71c5",
                        "1.2.4.A.3": "f977463d-53a7-4a59-b697-88688c0bee70",
                        "1.2.4.A.4": "de747279-87ff-4412-9358-de1fbb1719f9",
                    "1.2.4.B": "d31ac2ee-bbb4-4263-a67c-744c2a5c9d49",
                        "1.2.4.B.1": "eb4fcbe4-54c3-4bc6-b2a7-e16211edc95c",
                        "1.2.4.B.2": "2e4c9067-832a-4999-87f7-8c2750e010f0",
                        "1.2.4.B.3": "39844a26-e50d-42fc-bd39-3a8cf538ee97",
                    "1.2.4.C": "b8ee71cb-4c0a-4760-950c-a8a57a6100d2",
                        "1.2.4.C.1": "88776af5-adce-4a46-8f45-505742a072f8",
                        "1.2.4.C.2": "4a173b1a-693f-46ca-a79d-98e9d9a70649",
                        "1.2.4.C.3": "de61dd31-c11c-4413-b18f-cd5495c69143",
                        "1.2.4.C.4": "4ec3fd5d-2e30-4484-9952-6ae357e545d1",
                        "1.2.4.C.5": "dc22e5bf-c418-4b22-82ba-e39f8e0a5134",
            "Competency 1.3": "0d63add6-b202-42e2-8564-8171d086d050",
                "Micro 1.3.1": "16870b6d-bac4-4f2a-b137-7d5dde4fdf2e",
                    "1.3.1.A": "dd242598-04ca-4546-a7e7-e387c51af09e",
                        "1.3.1.A.1": "49da5a50-8a28-4852-97cc-488584161ad5",
                        "1.3.1.A.2": "1a771e55-bc78-4614-9e67-b7c7e6d8692e",
                    "1.3.1.B": "56b6be3d-7978-4480-a707-5f1ac8e83f34",
                        "1.3.1.B.1": "d72b220f-8c2c-46d9-a232-43d2b8574b10",
                    "1.3.1.C": "2c4e278a-654b-4311-9c54-86c169961faa",
                "Micro 1.3.2": "b5a1272c-a457-4258-b115-e62de0c78566",
                    "1.3.2.A": "5e5a59b5-58d2-4017-b7d6-6c8aac6d9eb0",
                        "1.3.2.A.1": "a52712b3-f0f2-4d47-9c8e-eccc6bbc0cf8",
                    "1.3.2.B": "0cbdabb5-babb-4037-b120-f34b35f0e63f",
                        "1.3.2.B.1": "b63ad8f0-ff00-41f7-907b-328a7931a9c5",
                    "1.3.2.C": "e154fa0d-10fc-4fcb-abd9-a52e4270ad3d",
                            "1.3.2.C.1": "3d64b1e2-bec7-4af3-8b66-41f25954da7a",
        "Macro 2.": "f3ffc136-e3a8-4c17-8e28-030b96d06bc9",
            "Competency 2.1": "48f850a1-2b64-488d-9ad9-5c00d62807fa",
                "Micro 2.1.1": "263f07f4-09d9-4f1f-9668-981cf16e6bad",
                    "2.1.1.A": "252fe683-0695-49cb-a448-ced759c8fe51",
                        "2.1.1.A.1": "d1edc98e-4da4-4ad2-b9dc-265e55e6b05a",
                        "2.1.1.A.2": "db57aa4e-5564-4984-8a36-a8b6a5a875c9",
                        "2.1.1.A.3": "d6b02fac-1d98-4882-8db0-75f589bae11d",
                    "2.1.1.B": "64462577-9725-47d9-b936-e6d36ebb7a05",
                        "2.1.1.B.1": "d7d6a698-0e50-4d39-838e-fe66c97a73f8",
                    "2.1.1.C": "878c9686-b7d3-4ef3-8cee-126525eb3593",
                "Micro 2.1.2": "837311dd-0421-479e-98e3-c42def1d63a0",
                    "2.1.2.A": "b096b07c-139b-4f31-b505-017e8cc35ba1",
                        "2.1.2.A.1": "46168406-165d-4fba-951f-62703b5ad6f4",
                        "2.1.2.A.2": "d076bc7f-fcf3-410f-994e-c2495f7dfdc7",
                        "2.1.2.A.3": "07da3bc7-9454-4c3e-a360-feadb3b166d8",
                        "2.1.2.A.4": "2441ca63-93c4-4320-9973-775999a3ef2e",
                        "2.1.2.A.5": "902bb3ee-8e58-4829-9777-77d9932d3fe6",
                    "2.1.2.B": "b63a509d-36c2-47da-8ec2-eefa9265710d",
                        "2.1.2.B.1": "4e46dbd3-bc4f-4855-831d-57cf3f089e75",
                        "2.1.2.B.2": "c46fd15c-d15e-4d4a-bf44-5c61ee94bb87",
                        "2.1.2.B.3": "fa547a1e-b401-422a-b6b4-34ce95e10c1f",
                        "2.1.2.B.4": "9eb84d33-ce20-4555-9685-65155dfde9ed",
                        "2.1.2.B.5": "8fc960d9-b589-4170-93a8-3de9a830873c",
                        "2.1.2.B.6": "8e4d88ac-31c3-4ae0-a82f-7b394498a9a7",
                    "2.1.2.C": "d2c27d0e-88b0-411c-8cd2-860b63c43238",
                        "2.1.2.C.1": "5cba4a80-a42e-4fba-ab50-e38fefdc9e51",
                        "2.1.2.C.2": "6b2648c5-bac4-4b97-9b74-0791159e200c",
                "Micro 2.1.3": "f090c2aa-4d20-439a-85ba-c885a453e010",
                    "2.1.3.A": "f0e26443-7a4d-4c56-a55c-bb332624ba9f",
                        "2.1.3.A.1": "ab48fa30-55d6-4fbb-8805-08cffaded05e",
                        "2.1.3.A.2": "4b80add8-6045-4aa9-a68f-80744e464363",
                    "2.1.3.B": "9695a6e3-558b-40d3-bb17-c54f12cfffb3",
                        "2.1.3.B.1": "4320d75e-3772-4ed7-94f9-99c7529a7960",
                    "2.1.3.C": "ad31bcb2-1e01-4f78-a90d-f6d9882878eb",
                        "2.1.3.C.1": "87e181c7-fe95-42c3-95aa-cdd044632b9a",
                        "2.1.3.C.2": "b365d135-dcd4-4dc2-9199-f900bcd2cb4b",
            "Competency 2.2": "22a3ce1f-51a7-490b-85f4-ec07e0294cc5",
                "Micro 2.2.1": "b1d8e1eb-55ae-4167-bdfd-1d3a29c8e27b",
                    "2.2.1.A": "5dbf4344-ae17-4f5d-8fce-dfd9adcc584c",
                        "2.2.1.A.1": "c3303f00-2d6f-4479-ad91-88225a8df89d",
                        "2.2.1.A.2": "9626523e-f27a-455c-b8f7-c37d2be9559e",
                    "2.2.1.B": "247e3c02-de0c-40c6-a0fb-2f6d289b8711",
                        "2.2.1.B.1": "b79fe1ea-9bc5-469c-83da-aaa26e4e66e7",
                        "2.2.1.B.2": "6100bc57-3509-4195-894d-5f3139061c24",
                    "2.2.1.C": "9ae623c8-3ee1-48c2-af7a-3ec4ba183730",
                        "2.2.1.C.1": "eeeba56b-9eb0-4aff-969e-6d67538441fc",
                "Micro 2.2.2": "49758606-dcd4-422e-bf15-c5a2fc2eef11",
                    "2.2.2.A": "657adc25-2bcf-4e0c-82ca-58d8838bc78e",
                        "2.2.2.A.1": "b25463d9-5f2b-4f8c-a178-03a45758625f",
                        "2.2.2.A.2": "2da2815d-df2e-4c27-81b0-b050219522d0",
                    "2.2.2.B": "dbf60bdb-255d-4309-8429-e5c92bf1c1a3",
                        "2.2.2.B.1": "a5535ffc-4a08-47e6-bc88-4ba1c3ce4610",
                        "2.2.2.B.2": "b2410c2b-20ff-4739-aa08-f01f3a80210e",
                        "2.2.2.B.3": "b5abe009-511c-445c-877b-03ff17ae16d2",
                    "2.2.2.C": "2c5e8d4a-64dd-472a-9423-9875477f9663",
                        "2.2.2.C.1": "1bea244f-ec59-4453-825c-eb2eb9f1d8c1",
        "Macro 3": "73c44cc8-6113-479e-8cc8-77829df857f9",
            "Competency 3.1": "a94f24da-bb5d-4493-9eb7-864529fdc644",
                "Micro 3.1.1": "15476476-6e0d-4ee0-bd09-61927298570e",
                    "3.1.1.A": "2b0667ca-2bb1-4ce5-8b97-8e840ec2b1ed",
                        "3.1.1.A .1": "72a6abd8-d061-484f-afdd-5a55a3c3b54f",
                    "3.1.1.B": "930babbe-5dfb-442b-899e-dd8868e944f7",
                        "3.1.1.B.1": "ffff78a4-2f2b-4729-ad63-b33c7209955e",
                    "3.1.1.C": "d5bccfd0-8c43-4d5c-a739-25d3d2dfb376",
                        "3.1.1.C.1": "35c6086f-5505-4812-886a-baa48878f562",
                "Micro 3.1.2": "2bbbd81a-58af-4488-859d-924c9edadd26",
                    "3.1.2.A": "aac00c12-c640-4e1d-8f77-ada6e5805c7f",
                        "3.1.2.A.1": "16501067-6ded-41af-a000-05a1a1c4da35",
                        "3.1.2.A.2": "2f9992a4-9a64-4c97-8f68-c5a49442af94",
                        "3.1.2.A.3": "61ef1327-8d12-4a65-ba39-6226d41f91b7",
                        "3.1.2.A.4": "4c93414e-fd6f-4242-bb46-2d59de1a52a1",
                        "3.1.2.A.5": "55b0939b-9215-4409-ba3f-b31ef9c3f311",
                        "3.1.2.A.6": "5a0c51aa-4f5e-441e-92ff-334b806e2aeb",
                        "3.1.2.A.7": "d47b6abd-8195-406b-8d75-f3a5b9e9d160",
                        "3.1.2.A.8": "8e4f5086-76ae-4620-8bfa-6609fa6f5758",
                    "3.1.2.B": "fd35a5aa-599d-4e46-ac18-99574eb64a3b",
                        "3.1.2.B.1": "0b2ee60c-8a42-4233-8428-43bb77338e6e",
                        "3.1.2.B.2": "c3c5b120-56ca-4fa3-a5e4-e3070ccf2f78",
                        "3.1.2.B.3": "0d236a73-5ac3-48a1-970f-07c9d9d6baee",
                        "3.1.2.B.4": "6e70284b-1e87-4557-be4f-de69a23e8a31",
                    "3.1.2.C": "f8cdf221-ef8e-4ec9-a2f4-6d23fbfd27ec",
                        "3.1.2.C.1": "b0d14ebd-801b-4f15-813a-e91bb78fd7ca",
                        "3.1.2.C.2": "9d609bff-ff88-431c-8a79-6f6c529185d1",
                "Micro 3.1.3": "0ee45b8f-cc32-4d5e-8cc1-aa045a8b74ce",
                    "3.1.3.A": "12889c48-4b5c-4c46-8bf7-b789345a85ec",
                        "3.1.3.A.1": "09d78141-1c3a-4384-855f-a1b03fd1f933",
                    "3.1.3.B": "a44b0547-5d0b-475d-bb76-4fbf50ec66a7",
                        "3.1.3.B.1": "0835c14e-e6cb-4991-8920-6fbeeee806e7",
                        "3.1.3.B.2": "219faa55-b3d6-4d90-b712-d45cc097c663",
                        "3.1.3.B.3": "0a682fc7-cbde-43c5-abf6-51faaced535b",
                        "3.1.3.B.4": "d097c101-3560-4173-ad5e-51a3b891f1cc",
                    "3.1.3.C": "32390d98-bbbf-416f-ace6-5f25fb3749b1",
                        "3.1.3.C.1": "7badf8b2-d945-42ab-bde2-bfcb310fe3bb",
                        "3.1.3.C.2": "1d86298e-87c6-4c09-a0ca-76eace12381c",
                        "3.1.3.C.3": "6e13a426-a109-432c-8126-f386ec3bb352",
                        "3.1.3.C.4": "033ff2dd-a7a2-4e85-82eb-0b7bff27b46a",
                "Micro 3.1.4": "34a06480-fe11-4c99-82d7-17ccd3653923",
                    "3.1.4.A": "c20184ba-5be2-4b9f-b5a5-6930871b863a",
                        "3.1.4.A.1": "ee4583f4-a3eb-473a-92fa-5ecee7cabc11",
                    "3.1.4.B": "527f8343-c1af-44fd-9767-af52f7133d88",
                        "3.1.4.B.1": "098f9492-1246-4896-ae70-725b07e83eea",
                    "3.1.4.C": "70b58e4a-077e-4868-bf76-8e8e5c947566",
                        "3.1.4.C.1": "e4af7cdf-a4d4-4cd9-9295-e592d126a1b1",
            "Competency 3.2": "a2f6903d-8a73-44c3-8c53-853f7db30dc6",
                "Micro 3.2.1": "66e947de-79b6-43ae-a48c-c0d702f7e86c",
                    "3.2.1.A": "98255e82-91f3-4901-a9c0-bdaf9cd9acbf",
                        "3.2.1.A.1": "c90f01ff-3341-4930-b871-c3e0ab1c3e31",
                    "3.2.1.B": "472e283c-9498-4a6a-9525-9f5455206dbb",
                        "3.2.1.B.1": "a99f9081-d947-44c5-8eee-5bca8207522c",
                    "3.2.1.C": "f68ad70e-6555-40cb-a154-57080d31aad8",
                        "3.2.1.C.1": "70c3ee4b-3cee-4c1f-acbd-cb253d1745c6",
                "Micro 3.2.2": "92ee20ea-d2ac-425e-be3f-9895038b2e24",
                    "3.2.2.A": "95a18350-1c5f-46ee-be5e-ab1cff67959f",
                        "3.2.2.A.1": "8ea04e57-4c4d-4a20-8211-dfe7783b9205",
                        "3.2.2.A.2": "2003c51d-be03-48d1-8d13-19a8be36e46a",
                    "3.2.2.B": "42b5bace-5a62-4e86-920d-7e52a905fd42",
                        "3.2.2.B.1": "5d9d3ca9-5182-45e1-8393-d632baa54afd",
                        "3.2.2.B.2": "bf0d159c-be77-48f5-b72e-ef53fb10d135",
                        "3.2.2.B.3": "5a4066b7-9569-4464-8e35-06226bb2b65f",
                    "3.2.2.C": "001097ef-e35c-4093-97c3-0953c55f0ed8",
                        "3.2.2.C.1": "567b7291-381f-4324-83d9-8dbc0a51a456",
                        "3.2.2.C.2": "0e176421-613f-4ed6-946b-f8e20bf63bbf",
                        "3.2.2.C.3": "f49dac2b-e28e-49c5-81bd-14b2dfaef2c1",
                "Micro 3.2.3": "70d028c7-6759-42de-9601-a2f21c4d3237",
                    "3.2.3.A": "349e5c81-ef91-4aff-b63a-aa3496844b0f",
                        "3.2.3.A.1": "92b0d230-0d85-4d52-8d0b-00460b0e5adb",
                    "3.2.3.B": "c631b687-ddd2-4f63-9c8e-8ab459ae882c",
                        "3.2.3.B.1": "b0d87627-42a6-4b3a-8744-b6ccda5390e8",
                    "3.2.3.C": "a3ba47b8-f7ea-43a4-b7aa-186a4c436e64",
                        "3.2.3.C.1": "9c623d2d-5310-4bfa-8edf-da64f3930f9b",
                        "3.2.3.C.2": "b362adf1-4101-42cf-b679-37afc36a496c",
                        "3.2.3.C.3": "220c4aa8-ddb6-49e6-8e89-d2018250dd13",
                "Micro 3.2.4": "071411ba-9b74-4b25-9788-c88aeb279b49",
                    "3.2.4.A": "76c667e9-8b7d-43d9-a322-8ddbe0976adc",
                        "3.2.4.A.1": "ef7e124b-c1c5-41cb-b8ef-903ec8324c71",
                        "3.2.4.A.2": "135370a8-d62c-448e-afe4-8a22dae8d97b",
                        "3.2.4.A.3": "d064dd79-ebb8-4dce-9d66-97b8c6adf4b4",
                        "3.2.4.A.4": "31003e16-62cc-45d5-b0f3-c20d7e374d31",
                    "3.2.4.B": "9f96b291-ba24-4d9d-8e87-f6ec01ee35c1",
                        "3.2.4.B.1": "3cebf418-c9ee-42c7-a7f1-c2f68b9dae98",
                    "3.2.4.B.2": "798ca0a0-df92-42d8-be06-57ea83633fba",
                        "3.2.4.B.3": "0bde2862-01a7-4bcd-9384-ffd8f4349656",
                    "3.2.4.C": "8f1e37de-4f1b-41c3-b9f6-8f0f978a7b8c",
                        "3.2.4.C.1": "2259be03-afb8-44d9-a823-9d6855ae5241"
    }

    @classmethod
    def setUpClass(cls):
        cls.cass_graph = load_or_instantiate('cass_graph_client.test.resources', CassGraph,
                                             '603d5ac2-fa9e-43c3-9c50-87ff65804ccd')  # type: CassGraph

    def test_unmastered_unblocked_descendants_just_leaves_at_micro_with_1_1_1_1_A_masterd(self):
        self._test_competencies(
            goal_competency_name='Micro 1.1.1',
            mastery_names=['1.1.1.A', '1.1.1.A.1', '1.1.1.A.2'],
            expected_competency_names=['1.1.1.B.1'],
            ancestors=False,
            only_leaves=True
        )

    def test_unmastered_unblocked_descendants_just_leaves_at_macro_new_learner(self):
        self._test_competencies(
            goal_competency_name='Macro 1.',
            mastery_names=[],
            expected_competency_names=[
                "1.1.1.A.1",
                "1.1.1.A.2",
                "1.1.2.A.1",
                "1.1.2.A.2",
                "1.1.3.A.1",
                "1.1.3.A.2",
                "1.2.1.A.1",
                "1.2.1.A.2",
                "1.2.2.A.1",
                "1.2.3.A.2",
                "1.2.3.A.3",
                "1.2.4.A.1",
                "1.2.4.A.2",
                "1.2.4.A.3",
                "1.2.4.A.4",
                "1.3.1.A.1",
                "1.3.1.A.2",
                "1.3.2.A.1"
            ],
            only_leaves= True,
            ancestors=False
        )


    def test_unmastered_unblocked_descendants_new_learner(self):
        self._test_competencies(
            goal_competency_name='Macro 1.',
            mastery_names=[],
            expected_competency_names=[
                "Competency 1.1",
                    "Micro 1.1.1",
                        "1.1.1.A",
                            "1.1.1.A.1",
                            "1.1.1.A.2",
                    "Micro 1.1.2",
                        "1.1.2.A",
                            "1.1.2.A.1",
                            "1.1.2.A.2",
                    "Micro 1.1.3",
                        "1.1.3.A",
                            "1.1.3.A.1",
                            "1.1.3.A.2",
                "Competency 1.2",
                    "Micro 1.2.1",
                        "1.2.1.A",
                            "1.2.1.A.1",
                            "1.2.1.A.2",
                    "Micro 1.2.2",
                        "1.2.2.A",
                            "1.2.2.A.1",
                    "Micro 1.2.3",
                        "1.2.3.A",
                            "1.2.3.A.2",
                            "1.2.3.A.3",
                    "Micro 1.2.4",
                        "1.2.4.A",
                            "1.2.4.A.1",
                            "1.2.4.A.2",
                            "1.2.4.A.3",
                            "1.2.4.A.4",
                "Competency 1.3",
                    "Micro 1.3.1",
                        "1.3.1.A",
                            "1.3.1.A.1",
                            "1.3.1.A.2",
                    "Micro 1.3.2",
                        "1.3.2.A",
                            "1.3.2.A.1"
            ],
            ancestors=False,
            only_leaves=False
        )

    def test_prerequisites_met(self):
        request_competency_id = self.competencies["1.1.1.B"]
        mastery_ids = [
            self.competencies['1.1.1.A']
        ]

        self.assertTrue(self.cass_graph.prerequisites_met(self.cass_graph.get_obj_by_id(request_competency_id), mastery_ids))

        mastery_ids = []
        self.assertFalse(self.cass_graph.prerequisites_met(self.cass_graph.get_obj_by_id(request_competency_id), mastery_ids))

    def test_unblocked_umastered_ancestors(self):
        self._test_competencies(
            goal_competency_name='1.1.1.B.1',
            mastery_names=[],
            expected_competency_names=['1.1.1.A.1', '1.1.1.A.2'],
            ancestors=True
        )

    def test_always_get_novice_for_new_learner(self):
        self._test_competencies(
            goal_competency_name='1.1.1.C',
            mastery_names=[],
            expected_competency_names=['1.1.1.A.1', '1.1.1.A.2'],
            ancestors=True,
            only_leaves=False
        )

        self._test_competencies(
            goal_competency_name='1.1.1.B',
            mastery_names=[],
            expected_competency_names=['1.1.1.A.1', '1.1.1.A.2'],
            ancestors=True,
            only_leaves=False
        )

        self._test_competencies(
            goal_competency_name='1.1.1.A',
            mastery_names=[],
            expected_competency_names=['1.1.1.A.1', '1.1.1.A.2'],
            ancestors=True,
            only_leaves=False
        )

        self._test_competencies(
            goal_competency_name='Micro 1.1.1',
            mastery_names=[],
            expected_competency_names=['1.1.1.A', '1.1.1.A.1', '1.1.1.A.2'],
            ancestors=False,
            only_leaves=False
        )

        self._test_competencies(
            goal_competency_name='Competency 1.1',
            mastery_names=[],
            expected_competency_names=[
                'Micro 1.1.1',
                    '1.1.1.A',
                        '1.1.1.A.1',
                        '1.1.1.A.2',
                'Micro 1.1.2',
                    '1.1.2.A',
                        '1.1.2.A.1',
                        '1.1.2.A.2',
                'Micro 1.1.3',
                    '1.1.3.A',
                        '1.1.3.A.1',
                        '1.1.3.A.2'
            ],
            ancestors=False,
            only_leaves=False
        )

        self._test_competencies(
            goal_competency_name='Macro 1.',
            mastery_names=[],
            expected_competency_names=[
                'Competency 1.1',
                    'Micro 1.1.1',
                        '1.1.1.A',
                            '1.1.1.A.1',
                            '1.1.1.A.2',
                    'Micro 1.1.2',
                        '1.1.2.A',
                            '1.1.2.A.1',
                            '1.1.2.A.2',
                    'Micro 1.1.3',
                        '1.1.3.A',
                            '1.1.3.A.1',
                            '1.1.3.A.2',
                'Competency 1.2',
                    'Micro 1.2.1',
                        '1.2.1.A',
                            '1.2.1.A.1',
                            '1.2.1.A.2',
                    'Micro 1.2.2',
                        '1.2.2.A',
                            '1.2.2.A.1',
                    'Micro 1.2.3',
                        '1.2.3.A',
                            '1.2.3.A.2',
                            '1.2.3.A.3',
                    'Micro 1.2.4',
                        '1.2.4.A',
                            '1.2.4.A.1',
                            '1.2.4.A.2',
                            '1.2.4.A.3',
                            '1.2.4.A.4',
                'Competency 1.3',
                    'Micro 1.3.1',
                        '1.3.1.A',
                            '1.3.1.A.1',
                            '1.3.1.A.2',
                    'Micro 1.3.2',
                        '1.3.2.A',
                            '1.3.2.A.1'
            ],
            ancestors=False,
            only_leaves=False
        )



    def _test_competencies(self, goal_competency_name: str, mastery_names: List[str],
                           expected_competency_names: List[str], ancestors: bool = False, only_leaves: bool = True):
        request_competency_id = self.competencies[goal_competency_name]
        mastery_ids = [self.competencies[name] for name in mastery_names]

        expected_unmastered_unblocked_ids = {
            self.cass_graph.get_obj_by_id(self.competencies[name]).id for name in expected_competency_names
        }

        if ancestors:
            competencies = self.cass_graph.get_unblocked_unmastered_ancestors(
                self.cass_graph.get_obj_by_id(request_competency_id),
                mastery_ids, only_leaves=only_leaves)
        else:
            competencies = self.cass_graph.get_unblocked_unmastered_descendants(
                self.cass_graph.get_obj_by_id(request_competency_id),
                mastery_ids, only_leaves=only_leaves)
        competency_ids = set([c.id for c in competencies])

        err_msg = self._error_message(competencies, expected_unmastered_unblocked_ids)

        self.assertEqual(expected_unmastered_unblocked_ids, competency_ids, err_msg)

    def _error_message(self, actual_competencies, expected_ids):
        expected_names = '\n\t'.join(
            sorted([c.ceasncoded_notation for c in [self.cass_graph.get_obj_by_id(cid) for cid in
                                                    expected_ids]]))
        actual_names = '\n\t'.join(sorted([competency.ceasncoded_notation for competency in actual_competencies]))
        error_msg = '\n\nExpected:\n\t{}\n\nActual:\n\t{}'.format(expected_names, actual_names)
        return error_msg

    def test_print_graph(self):
        print(str(self.cass_graph))
