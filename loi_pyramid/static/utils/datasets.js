import parseResponse from '../utils/xhr.js';

class Dataset {
	constructor(name, retrieve) {
		this.name = name;
		this.retrieve = retrieve;
	}

	getData(parentData) {
		let data = sessionStorage.getItem(`${this.name}`);
		if (!data) {
				return this.retrieve(parentData).then( data => {
					sessionStorage.setItem(`${this.name}`, JSON.stringify(data));
					return data; 
				});
		} else {
			return new Promise((resolve, reject) => { 
				return new Promise((resolve,reject) => { 
					resolve(JSON.parse(data))
				})
			})
		}
	}
}

var account = new Dataset(
	'account',
	function () {
		window.location = "login_stub.html"
	}
	);

var accountCharacters = new Dataset(
	'accountCharacters',
	function (account) {
		if (account && account.username) {
			console.log('fuck1');
			return fetch(`http://sundred.com:6543/accounts/${account.username}/characters`)
			.then( response => { 
				console.log('fuck2');
				return parseResponse(response)
				.then( characters => { 
					console.log('fuck4');
					return characters 
				}) 
			})
			.catch( error => {})
  	}
  });

export default { Dataset, account, accountCharacters };