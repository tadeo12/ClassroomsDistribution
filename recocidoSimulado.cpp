#include <iostream>
#include <vector>
#include <cmath>
#include <cstdlib> // Para rand()
#include <ctime>   // Para srand()
#include <algorithm> // Para random_shuffle
#include <map>
#include <string>
#include <set>

using namespace std;

struct Aula{
    
    int id;
    int capacidad;

    Aula(int id, int capacidad) : id(id), capacidad(capacidad) {}
};


// Estructura para representar un recurso (aula, día, hora)
struct Recurso {
    Aula aula;
    int dia;
    int hora;
    
    Recurso() : aula(Aula(0, 0)), dia(0), hora(0) {}

    Recurso(Aula aula, int dia, int hora) : aula(aula), dia(dia), hora(hora) {}

     // Sobrecargar el operador < para usar en std::set
    bool operator<(const Recurso& other) const {
        if (aula.id != other.aula.id) {
            return aula.id < other.aula.id;
        }
        if (dia != other.dia) {
            return dia < other.dia;
        }
        return hora < other.hora;
    }
};

struct Profesor {
    string nombre;
    Profesor(string nombre) : nombre(nombre) {}
};

struct Materia {
    string nombre;
    Materia(string nombre): nombre(nombre) {}
};

struct Comision {
    int alumnos;
    Profesor profesor;
    Materia materia;

    Comision(int alumnos, Profesor profesor, Materia materia): alumnos(alumnos), profesor(profesor), materia(materia) {}
};

// Estructura para representar un dictado (comisión y cantidad de alumnos)
struct Dictado {
    Comision* comision;
    int id;
    Dictado(Comision* comision, int id) : comision(comision), id(id) {}

     // Sobrecarga del operador < para utilizar Dictado como clave en std::map
    bool operator<(const Dictado& other) const {
        if (comision == other.comision) {
            return id < other.id;
        }
        return comision < other.comision;  // Compara punteros
    }
};


vector<Dictado> generarDictados(const vector<Comision>& comisiones) {
    vector<Dictado> dictados;
    for (const auto& comision : comisiones) {
        dictados.push_back(Dictado(const_cast<Comision*>(&comision),1));  // c1
        dictados.push_back(Dictado(const_cast<Comision*>(&comision),2));  // c2
    }
    return dictados;
};

// Función para generar recursos (aulas, días, horarios)
vector<Recurso> generarRecursos(const vector<Aula>& aulas, int dias, int horas) {
    vector<Recurso> recursos;
    for (const auto& aula : aulas) {
        for (int dia = 0; dia < dias; dia++) {
            for (int hora = 0; hora < horas; hora++) {
                recursos.emplace_back(aula, dia, hora);
            }
        }
    }
    return recursos;
};


map<Dictado, Recurso> generarDistribucionInicial(const vector<Dictado>& dictados, vector<Recurso>& recursos, set<Recurso>& recursosDisponibles) {
    map<Dictado, Recurso> distribucion;
    random_shuffle(recursos.begin(), recursos.end());

    for (size_t i = 0; i < dictados.size(); ++i) {
        distribucion.emplace(dictados[i], recursos[i]);
        recursosDisponibles.erase(recursos[i]); 
    }

    return distribucion;
};  


// Función para evaluar la calidad de la solución
int evaluar(const std::map<Dictado, Recurso>& distribucion) {
    int penalizacion = 0;

    for (const auto& d : distribucion) {
        const Dictado& dictado = d.first;
        const Recurso& recurso = d.second;

        // Penalización por capacidad del aula (si los alumnos superan la capacidad del aula)
        if (dictado.comision->alumnos > recurso.aula.capacidad) {
            penalizacion += 100; // Penalización por exceso de alumnos
        }



    }

    // Penalización por asignar c1 y c2 al mismo día
    for (auto it1 = distribucion.begin(); it1 != distribucion.end(); ++it1) {
        for (auto it2 = next(it1); it2 != distribucion.end(); ++it2) {
            const Dictado& dictado1 = it1->first;
            const Dictado& dictado2 = it2->first;

            // Si es la misma comisión y ambos dictados están en el mismo día
            if (dictado1.comision == dictado2.comision && it1->second.dia == it2->second.dia) {
                penalizacion += 1;  // Penalización por ambos dictados el mismo día
            }
        }
    }


    return penalizacion;
}



// Generar un vecino de la distribución actual con recursos disponibles como parámetro
map<Dictado, Recurso> generarVecino(map<Dictado, Recurso>& distribucion, set<Recurso>& recursosDisponibles) {
    map<Dictado, Recurso> vecino = distribucion;

    // Seleccionar aleatoriamente un dictado para cambiar su asignación de recurso
    auto it = vecino.begin();
    std::advance(it, rand() % vecino.size());
    const Dictado& dictado = it->first;

    // Recurso actualmente asignado que se liberará
    Recurso recursoActual = it->second;

    // Seleccionar aleatoriamente un recurso disponible para reasignarlo
    auto itRecursoDisponible = recursosDisponibles.begin();
    std::advance(itRecursoDisponible, rand() % recursosDisponibles.size());

    // Actualizar los recursos disponibles:
    // - Eliminar el nuevo recurso seleccionado de los disponibles
    Recurso nuevoRecurso = *itRecursoDisponible;
    recursosDisponibles.erase(itRecursoDisponible);
    
    // - Liberar el recurso actualmente asignado y añadirlo a los disponibles
    recursosDisponibles.insert(recursoActual);

    // Asignar el nuevo recurso al dictado
    vecino[dictado] = nuevoRecurso;

    return vecino;
}

// Algoritmo de Recocido Simulado
map<Dictado, Recurso> recocidoSimulado(const vector<Comision>& comisiones, const vector<Aula>& aulas, int iteraciones, double coefReduccionTemp, int dias, int horas) {
    vector<Dictado> dictados = generarDictados(comisiones);
    vector<Recurso> recursos = generarRecursos(aulas, dias, horas);

    set<Recurso> recursosDisponibles(recursos.begin(), recursos.end());

    // Generar la distribución inicial
    map<Dictado, Recurso> solucion = generarDistribucionInicial(dictados, recursos, recursosDisponibles);
    int costoSolucion = evaluar(solucion);
 
    map<Dictado, Recurso> actual = solucion;
    int costoActual = costoSolucion;
    double temperatura = 1.0;

    // Iteraciones de recocido simulado
    for (int i = 0; i < iteraciones; i++) {

        set<Recurso> recursosDisponiblesCopia = recursosDisponibles; //copia en profundida
        map<Dictado, Recurso> vecino = generarVecino(actual, recursosDisponiblesCopia); //actualiza los recursos disponibles en la copia
        int costoVecino = evaluar(vecino);

        int diferencia = costoVecino - costoActual;

        if (diferencia < 0 || exp(-diferencia / temperatura) > static_cast<double>(rand()) / RAND_MAX) {
            actual = vecino;
            costoActual = costoVecino;
            recursosDisponibles = recursosDisponiblesCopia;

            if (costoVecino < costoSolucion) {
                solucion = vecino;
                costoSolucion = costoVecino;
            } 
        }
        temperatura *= coefReduccionTemp;
    }

    return solucion;
}


// Función principal
int main() {
    srand(static_cast<unsigned int>(time(0))); // Inicializar semilla para números aleatorios

    // Ejemplo de comisiones
    vector<Comision> comisiones = {
        Comision(30, Profesor("Prof. Gomez"), Materia("Matematicas")),
        Comision(25, Profesor("Prof. Perez"), Materia("Fisica")),
        Comision(40, Profesor("Prof. Lopez"), Materia("Quimica")),
        Comision(30, Profesor("Prof. Gomez"), Materia("Matematicas2")),
        Comision(25, Profesor("Prof. Perez"), Materia("Fisica2")),
        Comision(40, Profesor("Prof. Lopez"), Materia("Quimica2")),
        Comision(30, Profesor("Prof. Gomez"), Materia("Matematicas3")),
        Comision(25, Profesor("Prof. Perez"), Materia("Fisica3")),
        Comision(40, Profesor("Prof. Lopez"), Materia("Quimica3"))
    };

    // Ejemplo de aulas
    vector<Aula> aulas = {
        Aula(1, 25), Aula(2, 30), Aula(3, 40)
    };

    // Parámetros del algoritmo
    int iteraciones = 1000;
    double coefReduccionTemp = 0.99; // Factor de enfriamiento
    int dias = 5;  // Días de la semana
    int horas = 2; // Horarios por día

    // Ejecutar el algoritmo de Recocido Simulado
    map<Dictado, Recurso> solucionFinal = recocidoSimulado(comisiones, aulas, iteraciones, coefReduccionTemp, dias, horas);


    int i=0; 
    // Imprimir la solución final
    for (const auto& pair : solucionFinal) {

        // cout << "Comision " << pair.first.comision->materia.nombre << " dictado " << pair.first.id 
        //      << " (alumnos: " << pair.first.comision->alumnos
        //      << ") asignada a aula " << pair.second.aula.id << " (capacidad: " << pair.second.aula.capacidad
        //      << "), dia " << pair.second.dia << ", hora " << pair.second.hora << endl;

        cout << "dictado " << i 
             << " (alumnos: " << pair.first.comision->alumnos
             << ") asignada a aula " << pair.second.aula.id << " (capacidad: " << pair.second.aula.capacidad
             << "), dia " << pair.second.dia << ", hora " << pair.second.hora << endl;

        i++;
    }
    
    int resultadoEvaluacion = evaluar(solucionFinal);
    cout << "Resultado de la evaluacion: " << resultadoEvaluacion << endl;


    return 0;
}
