"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { ChevronUp, ChevronDown } from "lucide-react"

const ResultItem = ({ label, value }) => (
    <div className="bg-gray-800/50 backdrop-blur-md rounded-xl p-3 sm:p-4 border border-gray-700/50 shadow-lg">
        <div className="text-xl sm:text-2xl font-bold text-gray-200">
            {typeof value === 'number'
                ? (Number.isInteger(value) ? value : value.toFixed(4))
                : value}
        </div>
        <div className="text-xs sm:text-sm text-right text-gray-400 mt-1 sm:mt-2">{label}</div>
    </div>
)

const CalcSection = ({ calc, title }) => (
    <div className="space-y-3 sm:space-y-4">
        <h3 className="text-lg sm:text-xl font-semibold text-gray-200">{title}</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
            <ResultItem label="Valor A" value={calc.value_a} />
            <ResultItem label="Valor Theta O" value={calc.value_theta_o} />
            <ResultItem label="Valor Theta" value={calc.value_theta} />
            <ResultItem label="Valor Q" value={calc.value_q} />
        </div>
    </div>
)

export default function ResultadosDrawer({ data }) {
    const [isOpen, setIsOpen] = useState(false)
    const [activeTab, setActiveTab] = useState("general")

    return (
        <div className={`fixed bottom-0 left-0 right-0 bg-gray-900/80 backdrop-blur-lg text-gray-200 rounded-t-3xl shadow-xl transition-all duration-300 ease-in-out ${isOpen ? 'h-[70vh]' : 'h-10'}`}>
            <div className="flex justify-center items-center h-10 cursor-pointer" onClick={() => setIsOpen(!isOpen)}>
                {isOpen ? <ChevronDown className="w-6 h-6" /> : <ChevronUp className="w-6 h-6" />}
                <span className="ml-2 text-lg sm:text-xl font-bold">Resultados</span>
            </div>

            {isOpen && (
                <div className="p-3 sm:p-4 md:p-6 overflow-y-auto h-[calc(70vh-2.5rem)]">
                    <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
                        <TabsList className="flex flex-wrap justify-center mb-4 bg-transparent">
                            {["general", "calculos", "lambda", "final"].map((tab) => (
                                <TabsTrigger
                                    key={tab}
                                    value={tab}
                                    className="px-3 py-2 m-1 text-xs sm:text-sm rounded-full bg-gray-800/50 text-gray-300 data-[state=active]:bg-blue-600/50 data-[state=active]:text-white transition-all duration-200 ease-in-out"
                                >
                                    {tab === "general" ? "General" :
                                        tab === "calculos" ? "Cálculos" :
                                            tab === "lambda" ? "Lambda" : "Resultados Finales"}
                                </TabsTrigger>
                            ))}
                        </TabsList>
                        <TabsContent value="general" className="mt-3 sm:mt-4">
                            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3 sm:gap-4">
                                <ResultItem label="Espesor" value={data.thickness} />
                                <ResultItem label="Difusividad térmica" value={data.thermal_diffusivity} />
                                <ResultItem label="Coeficiente de conductividad" value={data.conductivity_coefficient} />
                                <ResultItem label="Coeficiente de convección" value={data.convection_coefficient} />
                                <ResultItem label="Temperatura inicial" value={data.initial_temperature} />
                                <ResultItem label="Temperatura ambiente" value={data.ambient_temperature} />
                                <ResultItem label="Densidad" value={data.density} />
                                <ResultItem label="Calor específico" value={data.specific_heat} />
                                <ResultItem label="Distancia" value={data.distance} />
                                <ResultItem label="Tiempo" value={data.time} />
                                <ResultItem label="Iteraciones" value={data.iterations} />
                                <ResultItem label="Biot" value={data.biot} />
                                <ResultItem label="Geometría" value={data.geometry} />
                                <ResultItem label="Q Max" value={data.q_max} />
                            </div>
                        </TabsContent>
                        <TabsContent value="calculos" className="mt-3 sm:mt-4">
                            <div className="space-y-6 sm:space-y-8">
                                <CalcSection calc={data.calc1} title="Cálculo 1" />
                                <CalcSection calc={data.calc2} title="Cálculo 2" />
                                <CalcSection calc={data.calc3} title="Cálculo 3" />
                            </div>
                        </TabsContent>
                        <TabsContent value="lambda" className="mt-3 sm:mt-4">
                            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 sm:gap-4">
                                <ResultItem label="Lambda 1" value={data.lamb.lambda1} />
                                <ResultItem label="Lambda 2" value={data.lamb.lambda2} />
                                <ResultItem label="Lambda 3" value={data.lamb.lambda3} />
                            </div>
                        </TabsContent>
                        <TabsContent value="final" className="mt-3 sm:mt-4">
                            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3 sm:gap-4">
                                <ResultItem label="Valor A" value={data.value_a} />
                                <ResultItem label="Valor Theta O" value={data.value_theta_o} />
                                <ResultItem label="Valor Theta" value={data.value_theta} />
                                <ResultItem label="Valor Q" value={data.value_q} />
                                <ResultItem label="Temperatura" value={data.tem} />
                                <ResultItem label="Q" value={data.q} />
                            </div>
                        </TabsContent>
                    </Tabs>
                </div>
            )}
        </div>
    )
}