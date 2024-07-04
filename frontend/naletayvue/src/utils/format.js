export function formatCurrency(value, currency = 'RUB') {
    const numericValue = Number(value);
    if (isNaN(numericValue)) {
        return '';
    }

    return new Intl.NumberFormat('ru-RU', {
        style: 'currency',
        currency,
        minimumFractionDigits: 0,
        maximumFractionDigits: 0,
    }).format(numericValue);
}

export function convertCurrency(value, exchangeRate) {
    const numericValue = Number(value);
    if (isNaN(numericValue) || isNaN(exchangeRate)) {
        return '';
    }

    return numericValue * exchangeRate;
}