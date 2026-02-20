import { clsx } from "clsx";
import { twMerge } from "tailwind-merge"

/**
 * Función utilitaria para combinar clases de Tailwind sin conflictos
 * 
 * ¿Por qué existe?
 * - clsx: permite combinar clases condicionalmente de forma limpia
 * - twMerge: resuelve conflictos de Tailwind (ej: si tienes 'px-2' y 'px-4', 
 *   se queda con la última)
 * 
 * La combinación de ambas permite escribir clases condicionales sin preocuparse
 * por sobreescrituras o conflictos
 * 
 * @param {...any} inputs - Clases, objetos condicionales, arrays, etc.
 * @returns {string} Clases combinadas y resueltas
 */
export function cn(...inputs) {
  return twMerge(clsx(inputs));
}