import parseResponse from '../utils/xhr.js';

export class Dataset {
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
				resolve(JSON.parse(data))
			})
		}
	}
}

var account = new Dataset(
	'account',
	function (username) {
		if (username) {
			return fetch(`http://sundred.com:6543/accounts/${username}`)
			.then( response => { 
				return parseResponse(response)
			})
			.catch( error => {})
  	}
	}
);

var accountCharacters = new Dataset(
	'accountCharacters',
	function (account) {
		if (account && account.username) {
			return fetch(`http://sundred.com:6543/accounts/${account.username}/characters`)
			.then( response => { 
				return parseResponse(response)
			})
			.catch( error => {})
  	}
  }
 );

export default { Dataset, account, accountCharacters };