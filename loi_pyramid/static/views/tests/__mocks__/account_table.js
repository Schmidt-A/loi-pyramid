import Templates from '../../../utils/templates.js';
import { Dataset } from '../../../utils/datasets.js';
import accountTable from '../../account_table.js';

const testAccountTable = new Templates.Template( 
	new Dataset(
		'account',
		function () {
			return Promise.resolve(accountFixture);
		}),
	accountTable.markup,
	accountTable.renderData,
	accountTable.listeners
);

export default testAccountTable;