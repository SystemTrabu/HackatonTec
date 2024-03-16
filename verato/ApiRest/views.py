from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
import datetime
from faker import Faker
import random
import datetime
import random
from faker import Faker

global_text_data=None
global_json_data=None
global_types=None
global_count=None
global_porcentajetype=None
class JSONUploadView(APIView):
    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get('json_file')
        global global_text_data
        if not uploaded_file:
            return Response({'error': 'No se ha proporcionado ningún archivo'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            global global_json_data  # Acceder a la variable global
            # Lee el contenido del archivo JSON
            global_json_data = json.load(uploaded_file)
            print(global_text_data, 'probandoo')
            # Aquí puedes realizar cualquier operación con los datos JSON, como procesamiento, análisis, etc.
            return Response({'message': 'Archivo JSON subido exitosamente', 'data': global_json_data}, status=status.HTTP_201_CREATED)
        except json.JSONDecodeError:
            return Response({'error': 'El archivo subido no es un archivo JSON válido'}, status=status.HTTP_400_BAD_REQUEST)

class TextUploadView(APIView):
    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get('text_file')
        if not uploaded_file:
            return Response({'error': 'No se ha proporcionado ningún archivo'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            global global_text_data
            # Lee el contenido del archivo de texto
            text = uploaded_file.read().decode('utf-8')
            global_text_data=text.rstrip()
            # Aquí puedes realizar cualquier operación con los datos de texto
            
            
            return Response({'message': 'Archivo TXT subido exitosamente', 'data': global_text_data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': 'Error al procesar el archivo de texto: {}'.format(str(e))}, status=status.HTTP_400_BAD_REQUEST)


class Generate(APIView):
    def get(self, request, *args, **kwargs):
        global global_json_data
        global global_types
        global global_count
        global global_porcentajetype
        
        # Verificar si global_json_data no es nulo y si contiene la clave "cases"
        if global_json_data and 'cases' in global_json_data:
            global_count = global_json_data['records_per_arc']
            # Iterar sobre los casos en global_json_data
            for case in global_json_data['cases']:
                
                # Verificar si el caso es de tipo "FAMILY"
                if case['case_id'] == 'FAMILY':
                    # Obtener el valor de "distribution" y guardarlo en global_count
                    global_porcentajetype=case['distribution']
                    
                    # Inicializar un diccionario para almacenar los subcasos y sus distribuciones
                    family_distributions = {}
                    
                    # Iterar sobre los subcasos en el caso "FAMILY"
                    for sub_case in case['sub_cases']:
                        # Guardar el subcaso y su distribución en el diccionario
                        family_distributions[sub_case['case_id']] = sub_case['distribution']
                    
                    # Asignar el diccionario a global_types
                    global_types = family_distributions
                    print(global_types)  # Mostrar global_types en la consola
                    break  # Salir del bucle una vez que se haya encontrado el caso "FAMILY"
        
        Family.run()
        return Response({'message': 'Subcasos de FAMILY y sus distribuciones', 'data': family_distributions}, status=status.HTTP_200_OK)



class Family:
    estructura = 'ID|Prefix|FirstName|MiddleName|LastName|Suffix|Name Alias-1|Name Alias-2|Name Alias-3|DOB|SSN|Address-1 Line 1|Address-1 Line 2|Address-1 City|Address-1 State|Address-1 Zip|Address-1 Zip4|Address-2 Line 1|Address-2 Line 2|Address-2 City|Address-2 State|Address-2 Zip|Address-2 Zip4|Phone-1 Area Code|Phone-1 Base Number|Phone-2 Area Code|Phone-2 Base Number|Gender|SimilarityScore|CASE Type'

    # Semilla original
    #seed = "123ABC||STANFORD||SMITH||MD|SMITH,STANFORD|S,F,SMOTH||1965-01-09|343679845|123 MAIN ST||MOSCOW|ID|83844||456 ELM RD||MOSCOW|ID|83844||208|3450998|208|4569845|M||1.0|SEED"

    # Función para generar estructuras familiares
    @staticmethod
    def generate_family_structures(count, percentages):
        fake = Faker()
        family_change = []
        global global_text_data

        for _ in range(count):
            family_structure = global_text_data.split('|')  # Divide la semilla en partes
            type = Family.select_structure_type(percentages)
            if type == 'TWINS':
                genero = fake.random_element(['M', 'F'])
                
                if genero == 'F':
                    family_structure[2] = fake.first_name_female()
                    family_structure[28] = 'F'
                else:
                    family_structure[2] = fake.first_name_male()
                    family_structure[28] = 'M'

                ssn = family_structure[11]
                ssn_prefix = ssn[:-4] 
                ssn_suffix = ssn[-4:]  
                modified_suffix = list(ssn_suffix)  
                modified_suffix[random.randint(0, 3)] = str(fake.random_digit_or_empty())  
                new_ssn = ssn_prefix + ''.join(modified_suffix) 
                family_structure[11] = new_ssn  
                family_structure[31] = 'familary-twice'

            if type == 'PARENT_CHILD':
                genero = fake.random_element(['M', 'F'])

                if genero == 'F':
                    family_structure[2] = fake.first_name_female()
                    family_structure[28] = 'F'
                else:
                    family_structure[2] = fake.first_name_male()
                    family_structure[28] = 'M'

                fecha_nacimiento_original = datetime.datetime.strptime(family_structure[10], "%Y-%m-%d")
                nueva_fecha_nacimiento = fecha_nacimiento_original + datetime.timedelta(days=20*365)
                nueva_fecha_nacimiento_str = nueva_fecha_nacimiento.strftime("%Y-%m-%d")
                family_structure[10] = nueva_fecha_nacimiento_str

                if family_structure[6] == 'Jr':
                    numero = random.randint(0, 5)
                    if numero == 3:
                        family_structure[2] = 'Sr'
                        fecha_nacimiento_original = datetime.datetime.strptime(family_structure[10], "%Y-%m-%d")
                        nueva_fecha_nacimiento = fecha_nacimiento_original + datetime.timedelta(days=20*365)
                        nueva_fecha_nacimiento_str = nueva_fecha_nacimiento.strftime("%Y-%m-%d")
                        family_structure[10] = nueva_fecha_nacimiento_str

                if family_structure[6] == 'Sr':
                    numero = random.randint(0, 5)
                    if numero == 3:
                        family_structure[2] = 'Jr'
                        fecha_nacimiento_original = datetime.datetime.strptime(family_structure[10], "%Y-%m-%d")
                        nueva_fecha_nacimiento = fecha_nacimiento_original - datetime.timedelta(days=20*365)
                        nueva_fecha_nacimiento_str = nueva_fecha_nacimiento.strftime("%Y-%m-%d")
                        family_structure[10] = nueva_fecha_nacimiento_str

                family_structure[31] = 'familary-parent-child'

            if type == 'SIBLINGS':
                genero = fake.random_element(['M', 'F'])

                if genero == 'F':
                    family_structure[2] = fake.first_name_female()
                    family_structure[28] = 'F'
                else:
                    family_structure[2] = fake.first_name_male()
                    family_structure[28] = 'M'

                family_structure[31] = 'familary-siblings'

            family_change.append('|'.join(family_structure))

        return family_change

    # Función para seleccionar el tipo de estructura según los porcentajes
    @staticmethod
    def select_structure_type(percentages):
        rand_num = random.uniform(0, 100)
        cumulative_prob = 0

        for type, percentage in percentages.items():
            cumulative_prob += percentage
            if rand_num <= cumulative_prob:
                return type

    @staticmethod
    def run():
        global global_types
        global global_count
        global global_porcentajetype
        # Parámetros para la cantidad de estructuras a generar
        

        # Porcentajes de cada tipo de estructura
        if global_types is not None:
            percentages = global_types
            for key in percentages:
                percentages[key]*=100

        # Seleccionar y mostrar las estructuras
        if global_count is not None:
            print(global_count, 'ola')
            print(global_porcentajetype, 'ola')
            print(percentages)

            family_count=int(global_count*global_porcentajetype)
            # for key in percentages:
            #     percentages[key]*=100
            print(percentages, 'new')
            print(family_count)
            family_structures = Family.generate_family_structures(family_count, percentages)

            for family in family_structures:
                print (family)
                
            
            
        else:
            family_structures = Family.generate_family_structures(0, percentages)
        

class similares:
    @staticmethod
    def generate_similares_estructure(count, percentages):
        fake = Faker()
        family_change = []


