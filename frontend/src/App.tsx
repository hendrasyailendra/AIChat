import { useState } from 'react';

function App() {
	const [count, setCount] = useState(0);

	return (
		<>
			<div className='App'>
				<div className='text-8xl bg-blue-500'>Hello</div>
			</div>
		</>
	);
}

export default App;
