CREATE DATABASE VehiculosConjunto;	-- Creación de la base de datos de los vehiculos del conjunto.
GO									-- Ejecutar todo lo anterior antes de continuar.
USE VehiculosConjunto;				-- Todo lo que se haga será dentro de la base de datos creada.

CREATE TABLE VehiculosRegistrados (
	Id INT PRIMARY KEY IDENTITY (1,1),
	Placa NVARCHAR(6) UNIQUE NOT NULL,
	Nombre NVARCHAR(100) UNIQUE NOT NULL,
	Marca NVARCHAR (40) NOT NULL,
	Modelo NVARCHAR(25) NOT NULL,
	Color NVARCHAR(20) NOT NULL,
	Num_Parqueadero INT
);

CREATE TABLE VehiculosVisita (
	Id INT PRIMARY KEY IDENTITY (1,1),
	Placa NVARCHAR(6) UNIQUE NOT NULL,
	Nombre NVARCHAR(100) UNIQUE NOT NULL,
	Documento_Identidad NVARCHAR(15) NOT NULL,
	Marca NVARCHAR (40) NOT NULL,
	Apto_Destino INT,
	Fecha_Registro DATE DEFAULT GETDATE(),
	Hora_Registro TIME DEFAULT CONVERT(TIME, GETDATE())
);

CREATE TABLE Deteccion (
	Id INT PRIMARY KEY IDENTITY (1,1),
	Placa NVARCHAR(6) NOT NULL,
	Fecha_in DATE,
	Hora_in TIME,
	Nombre NVARCHAR(100),
	Marcar NVARCHAR(40),
	Num_Parqueadero INT
);