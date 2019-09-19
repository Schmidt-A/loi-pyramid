function parseResponse(response) {
	console.log(`fuck3 ${response.ok}`);
	if (response.ok) {
		return response.json();
	} else {
		console.error(response.status);
		throw new Error(response);
	}
}

export default parseResponse;