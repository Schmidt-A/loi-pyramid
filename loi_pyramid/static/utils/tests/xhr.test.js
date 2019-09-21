import parseResponse from '../xhr.js';
import mockFetch from '../../test_utils/mockFetch.js';

let mockData1 = {'mockKey': 1};

test('parseResponse()', async () => {
    jest.spyOn(window, 'fetch').mockImplementation( () => { return mockFetch(true, 200, mockData1) });

    let mockJson = await fetch('I wanna find some mock data')
    .then( mockResponse => { 
        return parseResponse(mockResponse) 
    });

    expect(mockJson).toBe(mockData1);
});

test('parseResponse() error', async () => {
    jest.spyOn(window, 'fetch').mockImplementation( () => { return mockFetch(false, 500) });
    
        let mockJson = await fetch('I wanna find some mock data')
        .then( mockResponse => {
            return parseResponse(mockResponse);
        }).catch( error => {
            expect(error instanceof Error).toBeTruthy();
        });
});