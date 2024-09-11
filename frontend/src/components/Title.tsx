import axios from 'axios';
import { useState } from 'react';

type Props = {
	setMessages: any;
};

const Title = ({ setMessages }: Props) => {
	const [isResetting, setIsResetting] = useState(false);

	const resetConversation = async () => {
		setIsResetting(true);
		await axios
			.get('http://localhost:8000/reset')
			.then((res) => {
				if (res.status === 200) {
					setMessages([]);
				} else {
					console.error('Reset failed');
				}
			})
			.catch((err) => console.error(err.messages));
		setIsResetting(false);
	};
	return (
		<div>
			<button className='bg-indigo-500 p-5' onClick={resetConversation}>
				RESET
			</button>
		</div>
	);
};

export default Title;
