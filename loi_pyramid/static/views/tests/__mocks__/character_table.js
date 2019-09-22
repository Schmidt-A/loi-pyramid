import Templates from '../../../utils/templates.js';
import { Dataset } from '../../../utils/datasets.js';
import characterTable from '../../character_table.js';

const testCharacterTable = new Templates.Template( 
	new Dataset(
		'accountCharacters',
		function () {
			return Promise.resolve(characterFixture);
		}),
	characterTable.markup,
	characterTable.renderData,
	characterTable.listeners
);

export default testCharacterTable;