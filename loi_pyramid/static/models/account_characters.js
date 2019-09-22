import { Dataset } from '../utils/datasets.js';

const accountCharactersData = new Dataset(
    'accountCharacters',
    function (account) {
        if (account && account.username) {
            return fetch(`http://sundred.com:6543/accounts/${account.username}/characters`)
            .then( response => { 
                if (response.ok) {
                    return response.json()
                }
            })
            .catch( error => {})
        }
    }
 );

export default accountCharactersData;