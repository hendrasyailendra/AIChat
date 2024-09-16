import axios from 'axios';
import { useState } from 'react';
import RecordMessage from './RecordMessage';
import Title from './Title';
const Controller = () => {
	const [isLoading, setIsLoading] = useState(false);
	const [messages, setMessages] = useState<any[]>([]);

	const createBlobUrl = (data: any) => {
		const blob = new Blob([data], { type: 'audio/mpeg' });
		const url = window.URL.createObjectURL(blob);
		return url;
	};

	const handleStop = async (blobUrl: string) => {
		setIsLoading(true);
		const myMessage = { sender: 'me', blobUrl };
		const messageArr = [...messages, myMessage];

		fetch(blobUrl)
			.then((res) => res.blob())
			.then(async (blob) => {
				const formData = new FormData();
				formData.append('file', blob, 'myFile.wav');
				await axios
					.post('http://localhost:8000/post-audio', formData, {
						headers: { 'Content-Type': 'audio/mpeg' },
						responseType: 'arraybuffer',
					})
					.then((res: any) => {
						const blob = res.data;
						const audio = new Audio();
						audio.src = createBlobUrl(blob);

						const AIMessage = { sender: 'rachel', blobUrl: audio.src };
						messageArr.push(AIMessage);
						setMessages(messageArr);
						console.log(messageArr);
						setIsLoading(false);
						audio.play();
					})
					.catch((err) => {
						console.error(err.message);
						setIsLoading(false);
					});
			});
	};

	return (
		<div className='h-screen overflow-y-hidden'>
			<Title setMessages={setMessages} />
			<div className='flex flex-col justify-between h-full overflow-y-scroll pb-96'>
				<div className='fixed bottom-0 w-full py-6 border-t text-center bg-gradient-to-r from-sky-500 to-green-500'>
					<div className='flex justify-center items-center w-full'>
						<RecordMessage handleStop={handleStop} />
					</div>
				</div>
			</div>
		</div>
	);
};

export default Controller;
