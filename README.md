# 🏗️ Plataforma interna de gestión de obras

Aplicación web interna para la gestión y seguimiento de obras de construcción.
Permite coordinar el trabajo entre administradores de obra y operarios, facilitando la asignación de tareas, el reporte de avances e incidencias y el control de disponibilidad del personal.

> ⚠️ Esta plataforma es de uso interno de la empresa.
> Los clientes o propietarios de las obras no tienen acceso.

---

# 👥 Roles de usuario

La aplicación dispone de dos tipos de acceso diferenciados:

## 👷 Operario / Trabajador

Usuarios encargados de ejecutar trabajos en obra.

**Funciones principales:**

- Consultar las obras asignadas
- Registrar avances de trabajo
- Reportar incidencias
- Solicitar materiales
- Marcar finalización de tareas
- Cambiar estado a _disponible_ al completar una obra

---

## 🧑‍💼 Administrador de obra

Responsable de planificación, seguimiento y asignación de personal.

**Funciones principales:**

- Acceder a todas las obras activas
- Crear nuevas obras
- Asignar operarios disponibles a obras
- Visualizar avances registrados
- Consultar incidencias reportadas
- Ver disponibilidad de trabajadores
- Gestionar estado de las obras

---

# 🔄 Flujo de trabajo

1. El administrador crea una obra.
2. El administrador asigna operarios disponibles.
3. Los operarios registran avances, incidencias y necesidades.
4. El administrador supervisa el progreso.
5. Al finalizar, el operario marca la obra como completada.
6. El operario vuelve a estado disponible.

---

# 🏗️ Conceptos clave

- **Obra:** Proyecto de construcción gestionado en la plataforma.
- **Operario disponible:** Trabajador sin obra asignada activa.
- **Incidencia:** Problema o bloqueo en la ejecución.
- **Avance:** Registro de progreso en la obra.
- **Solicitud de material:** Petición de recursos necesarios.

---

# 🔐 Acceso a la aplicación

El acceso se realiza mediante autenticación con credenciales de usuario.

Tipos de acceso:

- Administrador
- Operario

Las funcionalidades visibles dependen del rol.

---

# 🎯 Objetivo del sistema

Centralizar la gestión operativa de obras y personal de campo, permitiendo:

- Mejor coordinación interna
- Seguimiento en tiempo real
- Registro histórico de obras
- Optimización de recursos humanos
- Trazabilidad de incidencias y materiales

---

# 📌 Estado del proyecto

En desarrollo.

---

# 📄 Licencia

Uso interno de la empresa.

## PLUS NOTIFICACIONES Reglas de negocio clave

🔒 El operario solo ve/edita sus propias notificaciones
🧑‍💼 El admin ve todas las notificaciones de todas las obras
🗑️ Solo el admin puede eliminar notificaciones
🔍 Los filtros son opcionales — sin filtro devuelve todo lo permitido al rol
