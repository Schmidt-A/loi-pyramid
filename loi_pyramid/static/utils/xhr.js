async function parseResponse(response) {
	if (response.ok) {
		return await response.json();
	} else {
		console.error(response.status);
		throw new Error(response);
	}
}

export default parseResponse;