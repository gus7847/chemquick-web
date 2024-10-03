"use client"

import { useState } from "react"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Button } from "@/components/ui/button"
import ResultadosDrawer from "./ResultadosDrawer"

const apiURL = process.env.NEXT_PUBLIC_API_URL

const CustomInput = ({ label, value, onChange, name }) => (
    <div className="bg-gray-800/50 backdrop-blur-md rounded-xl p-3 sm:p-4 md:p-5 border border-gray-700/50 shadow-lg">
        <input
            type="text" // Cambiado a 'text' para permitir cualquier tipo de entrada
            value={value}
            onChange={onChange}
            name={name}
            className="w-full bg-transparent text-xl sm:text-2xl md:text-3xl font-bold text-gray-200 outline-none placeholder-gray-500"
            placeholder="0"
        />
        <div className="text-xs sm:text-sm md:text-base text-right text-gray-400 mt-1 sm:mt-2">
            {label}
        </div>
    </div>
)

export default function CalculadoraConveccion() {
    const [formData, setFormData] = useState({
        thickness: "",
        thermal_diffusivity: "",
        conductivity_coefficient: "",
        convection_coefficient: "",
        initial_temperature: "",
        ambient_temperature: "",
        density: "",
        specific_heat: "",
        distance: "",
        time: "",
        iterations: "",
        biot: "",
        geometry: "plate"
    })

    const [results, setResults] = useState(null)

    const handleInputChange = (e) => {
        const { name, value } = e.target
        setFormData(prev => ({ ...prev, [name]: value }))
    }

    const handleGeometryChange = (value) => {
        setFormData(prev => ({ ...prev, geometry: value }))
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        // Reemplaza los valores vacíos con 0
        const updatedFormData = Object.fromEntries(
            Object.entries(formData).map(([key, value]) => [key, value === "" ? "0" : value])
        )
        try {
            const response = await fetch(`${apiURL}/convection/calculate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(updatedFormData)
            })
            console.log(updatedFormData)
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json()
            setResults(data.data) // Actualiza el estado con los datos recibidos
        } catch (error) {
            console.error("Error al llamar a la API:", error)
        }
    }

    const fieldLabels = {
        thickness: "Espesor",
        thermal_diffusivity: "Difusividad térmica",
        conductivity_coefficient: "Coeficiente de conductividad",
        convection_coefficient: "Coeficiente de convección",
        initial_temperature: "Temperatura inicial",
        ambient_temperature: "Temperatura ambiente",
        density: "Densidad",
        specific_heat: "Calor específico",
        distance: "Distancia",
        time: "Tiempo",
        iterations: "Iteraciones",
        biot: "Número de Biot",
        geometry: "Geometría"
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-900 to-blue-900 flex items-center justify-center p-2 sm:p-4 md:p-6 font-sans">
            <form onSubmit={handleSubmit} className="bg-gray-800/30 backdrop-blur-lg text-gray-200 rounded-3xl shadow-xl p-4 sm:p-6 md:p-8 w-full max-w-7xl">
                <h2 className="text-2xl sm:text-3xl md:text-4xl font-bold mb-4 sm:mb-6 md:mb-8 text-center">CONVECCIÓN</h2>

                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3 sm:gap-4 md:gap-5">
                    {Object.entries(formData).map(([key, value]) => (
                        key !== 'geometry' ? (
                            <CustomInput
                                key={key}
                                label={fieldLabels[key]}
                                value={value}
                                onChange={handleInputChange}
                                name={key}
                            />
                        ) : null
                    ))}
                </div>

                <div className="mt-3 sm:mt-4 md:mt-5 bg-gray-800/50 backdrop-blur-md rounded-xl p-3 sm:p-4 md:p-5 border border-gray-700/50 shadow-lg">
                    <Select onValueChange={handleGeometryChange} defaultValue={formData.geometry}>
                        <SelectTrigger className="w-full bg-transparent text-xl sm:text-2xl md:text-3xl font-bold text-gray-200 border-none">
                            <SelectValue placeholder="Selecciona la geometría" />
                        </SelectTrigger>
                        <SelectContent className="bg-gray-800/90 backdrop-blur-md text-gray-200">
                            <SelectItem value="plate">Placa</SelectItem>
                            <SelectItem value="cylinder">Cilindro</SelectItem>
                            <SelectItem value="sphere">Esfera</SelectItem>
                        </SelectContent>
                    </Select>
                    <div className="text-xs sm:text-sm md:text-base text-right text-gray-400 mt-1 sm:mt-2">
                        {fieldLabels.geometry}
                    </div>
                </div>

                <Button type="submit" className="w-full mt-4 sm:mt-6 md:mt-8 mb-8 sm:mb-0 bg-gradient-to-r from-blue-600 to-teal-500 hover:from-blue-700 hover:to-teal-600 text-white text-lg sm:text-xl md:text-2xl font-bold py-3 sm:py-4 md:py-5 rounded-xl transition duration-300 ease-in-out shadow-lg">
                    Calcular
                </Button>
            </form>

            {results && <ResultadosDrawer data={results} />}
        </div>
    )
}