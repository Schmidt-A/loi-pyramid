async function parseResponse(response) {
    if (response.ok) {
        let data = await response.json();
        return data;
    } else {
    	console.log(response.status);
        throw new Error(response);
    }
}

export default parseResponse;