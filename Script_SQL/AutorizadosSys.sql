CREATE DATABASE UsuariosAutorizados;	-- Creaci�n de la base de datos de los directivos autorizados para ingresar al sistema.
GO										-- Ejecutar todo lo anterior antes de continuar.
USE UsuariosAutorizados;				-- Todo lo que se haga ser� dentro de la base de datos creada.

CREATE TABLE Autorizados (
	Id INT PRIMARY KEY IDENTITY(1,1),
	Usuario NVARCHAR(50) UNIQUE NOT NULL,
	Contrase�a NVARCHAR(255) UNIQUE NOT NULL,
	Nombre_Completo NVARCHAR(100) UNIQUE NOT NULL,
	Documento_Identificaci�n NVARCHAR(30) UNIQUE NOT NULL,
	Edad INT,
	Celular NVARCHAR(10) NOT NULL,
	Direccion NVARCHAR(40) NOT NULL,
	Rol NVARCHAR(50) NOT NULL,
	UltimoIni_Sesion DATETIME
);

INSERT INTO Autorizados (
    Usuario,
    Contrase�a,
    Nombre_Completo,
    Documento_Identificaci�n,
    Edad,
    Celular,
    Direccion,
    Rol,
    UltimoIni_Sesion
)
VALUES (
    'admin',
    '1234',  
    'Brenda P�rez',
    '100200300',
    28,
    '3012345678',
    'Torre A, Apto 302',
    'Administrador',
    NULL
);