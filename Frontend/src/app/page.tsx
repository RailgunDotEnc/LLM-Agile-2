'use client';
import Image from "next/image";
import {Box, Card, CardContent, FormControl, FormControlLabel, InputLabel, Typography} from "@mui/material";
import UploadFileIcon from '@mui/icons-material/UploadFile';
import CloseIcon from '@mui/icons-material/Close';
import axios from "axios";
import React, {useEffect, useRef, useState} from "react";
import SendRoundedIcon from '@mui/icons-material/SendRounded';
import ReactMarkdown from 'react-markdown';
import Skeleton from '@mui/material/Skeleton';
import {useUser} from "@auth0/nextjs-auth0/client";
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import InputAdornment from '@mui/material/InputAdornment';
import IconButton from '@mui/material/IconButton';
import Visibility from '@mui/icons-material/Visibility';
import VisibilityOff from '@mui/icons-material/VisibilityOff';
import DeleteIcon from '@mui/icons-material/Delete';
import SwapCallsIcon from '@mui/icons-material/SwapCalls';
import SettingsIcon from '@mui/icons-material/Settings';
import {v4 as uuidv4} from 'uuid';
import {
    AppInputBox,
    CustomButton,
    CustomButtonWithBackground,
    CustomButtonWithOutline,
    CustomSecondaryButtonWithBackground,
    DestructiveButtonWithBackground,
    HeroButtonWithBackground,
    PrimaryButtonWithBackground
} from "@/components/commons/Buttons";
import AddIcon from '@mui/icons-material/Add';
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import {Modal} from "@mui/base";
import {SaveAlt} from "@mui/icons-material";
import Select from '@mui/material/Select';


const style = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: '350px',
    bgcolor: 'background.paper',
    boxShadow: 24,
    p: 4,
    borderRadius: '10px',
};

export default function Home() {
    interface QuestionData {
        [key: string]: [string, string];
    }
    // TODO: Add the process.env read t
    const [loading, setLoading] = useState(false);
    const websiteKey = 'xyz' 
    const jiraAPIkey = '<key>'
    const [userKey, setUserKey] = useState<string>("12345abcde");
    const [PromptTitle, setPromptTitle] = useState<string>("");
    const [FormatTitle, setFormatTitle] = useState<string>("");
    const BaseURL = 'http://<ip>:<port>/api/';

    const [username, setUsername] = useState<string>('default');
    const AllPrompts = `${BaseURL}ScanAllPrompts?api_key=${websiteKey}${userKey}`
    const AllFormats = `${BaseURL}ScanAllFormats?api_key=${websiteKey}${userKey}`
    const FindPrompts = `${BaseURL}FindPrompt?api_key=${websiteKey}${userKey}&Title=${PromptTitle}`;
    const FindFormats = `${BaseURL}FindFormat?api_key=${websiteKey}${userKey}&Title=${FormatTitle}`;
    const RemovePrompt = `${BaseURL}RemovePrompt?api_key=${websiteKey}${userKey}&Username=${username}&Title=${PromptTitle}`;
    const RemoveFormat = `${BaseURL}RemoveFormat?api_key=${websiteKey}${userKey}&Username=${username}&Title=${FormatTitle}`;
    const [invalidate, setInvalidate] = useState(false);
    const [invalidate2, setInvalidate2] = useState(false);
    const QueryModel = `${BaseURL}Model?api_key=${websiteKey}${userKey}&Model=`;
    const [model, setModel] = useState<string>("gemini");
    const [inputValue, setInputValue] = useState('');
    const [email, setEmail] = useState('');
    const [projectKey, setProjectKey] = useState('');
    const [messages, setMessages] = useState<{ message: string, sender: string }[]>([])
    const [searchTerm, setSearchTerm] = useState('')
    const [model_history, setModel_history] = useState<any>({});
    const [modelObject, setModelObject] = useState<any>({});
    const [showPassword, setShowPassword] = React.useState(false);
    const [data, setData] = useState(null);
    const [data2, setData2] = useState(null);
    const [data3, setData3] = useState(null);
    const [data4, setData4] = useState(null);
    const [multiLLM, setMultiLLM] = useState<boolean>(false)
    const [currentTab, setCurrentTab] = useState<string>(model)
    const [samplehistory, setSamplehistory] = useState<string>(''); // State to store samplehistory
    const [sampleFormat, setSampleFormat] = useState<string>(''); // State to store sampleformat
    const [jiraModalOpen, setOpen] = React.useState(false);
    const handleOpen = () => setOpen(true);
    const handleClose = () => setOpen(false);
    const [formattedContent, setFormattedContent] = useState<React.ReactNode>(''); // State to store samplehistory
    const [modelHistoryDataString, setModelHistoryDataString] = useState<string>(''); // State for model history data string
    const [pTitleUUID, setPTitleUUID] = useState(uuidv4());
    const [PTitle, setPTitle] = useState<string>('');
    const [FTitle, setFTitle] = useState<string>('');
    const [Fformat, setFformat] = useState<string>(''); // State for model history data string
    const [SDLCNum, setSDLCNum] = useState<int>('1'); 
    const [secNum, setSecNum] = useState<int>('-1'); 


    const titleOfFile = Object.keys(data || {})[0] || '';
    const usersArray = Object.keys((data && data[titleOfFile]) || {}) || [];

    const titleOfFormat = Object.keys(data2 || {})[0] || '';
    const usersArray2 = Object.keys((data2 && data2[titleOfFormat]) || {}) || [];

    const models = [
        {
            label: "Chat GPT",
            value: 'gpt'
        },
        {
            label: "Google Gemini",
            value: 'gemini'
        },
        {
            label: "Claude",
            value: 'claude'
        },
        {
            label: "Llama",
            value: 'llama'
        },
    ]

    const formatDataString = ((data2 && data2[titleOfFormat] && data2[titleOfFormat][usersArray2[0]]) as string | null) || undefined


    const [selectedPrompt, setSelectedPrompt] = useState<string>(usersArray[0] || ''); // State for selected prompt
    const [selectedUser, setSelectedUser] = useState<string>(usersArray[0] || ''); // State for selected user
    const [selectedUser2, setSelectedUser2] = useState<string>(usersArray2[0] || ''); // State for selected user

    const [selectedModel, setSelectedModel] = useState<string>(models[0].label || '' ); // State for selected model
    const [selectedFormat, setSelectedFormat] = useState<string>(models[0].label || '' ); // State for selected model
    const handleUserChange = (event: any) => {
            const selectedUserValue = event.target.value;
            setSelectedUser(selectedUserValue); // Update selected user

            // Update model history data string based on the selected user
            const newModelHistoryDataString = JSON.stringify(
                ((data && data[titleOfFile] && data[titleOfFile][selectedUserValue]) as {
                    models?: any
                } | null)?.models || {}
            );
            setModelHistoryDataString(newModelHistoryDataString);

            // Also, update sample history and format questions if needed
            if (selectedModel) {
                const historyData = JSON.parse(newModelHistoryDataString)[selectedModel]?.model_history;
                const jsonString = JSON.stringify(historyData || {});
                setSamplehistory(historyData);
                formatQuestions(jsonString, selectedModel);
            }
        }
    ;

    const modelHistoryData = modelHistoryDataString ? JSON.parse(modelHistoryDataString) : {};
    const filteredModels = models.filter(model => Object.keys(modelHistoryData).includes(model.value));

    const handleUserChange2 = (event: any) => {
        setSelectedUser2(event.target.value);

    };


    const handleClickShowPassword = () => setShowPassword((show) => !show);

    const handleMouseDownPassword = (event: any) => {
        event.preventDefault();
    };

    const refToMonitor = useRef(null);
    const {user, error, isLoading} = useUser();
    const [anchorEl, setAnchorEl] = React.useState(null);
    const open = Boolean(anchorEl);
    const handleClick = (event: any) => {
        setAnchorEl(event.currentTarget);
    };
    const [jiraArray, setJiraArray] = useState<any[]>([]);


    useEffect(() => {
        if (!isLoading && user) {
            // If user exists, do something (like fetching messages, etc.)
            if (user?.name) {
                setUsername(user.name);
            }
        }
    }, [user, isLoading]);

    useAutoScroll(refToMonitor);
    const handleChange = (event: any) => {
        setInputValue(event.target.value);
    };

    function ChatBubble({text, sender}: any) {
        return (
            <div style={{paddingTop: '20px'}}>
                <Typography textAlign={sender === 'You' ? 'left' : 'right'} color={'grey'} fontFamily={'Chivo Mono'}
                            fontWeight={300} fontSize={'15px'}>{sender}</Typography>
                <div className={sender === 'You' ? "chat-bubble" : 'chat-bubble-response'}>
                    <ReactMarkdown>{text}</ReactMarkdown>
                </div>
            </div>
        );
    }

    const handleTitleChange = (event: any) => {
        setPromptTitle(event.target.value)
        setPTitle(event.target.value)

    };
    const handleTitleChange2 = (event: any) => {
        setFormatTitle(event.target.value)

    };
    const handleModelChange = (event: any) => {
        const selectedModelValue = event.target.value;
        setSelectedModel(selectedModelValue);


        // Parse model history data for the selected model
        const modelHistoryData = JSON.parse(modelHistoryDataString);

        console.log(modelHistoryData);
        const historyData = modelHistoryData[selectedModelValue]?.model_history;

        // Convert historyData to string and update samplehistory state
        const jsonString = JSON.stringify(historyData);
        setSamplehistory(historyData);
        formatQuestions(jsonString, selectedModelValue);

    };

    function formatQuestions(jsonString: string, selectedModelValue: string): void {
        try {
            const data: QuestionData = JSON.parse(jsonString);

            const formattedQuestions = Object.keys(data).map((key) => {
                const questionNumber = key.replace("_", " ");
                const question = data[key][0];
                const response = data[key][1];

                return (
                    <Card elevation={0}
                          sx={{minWidth: '90%', marginTop: '10px', border: '1px solid #000'}}>
                        <CardContent>
                            <Typography fontFamily={'Chivo Mono'} sx={{fontSize: 14}}
                                        color="text.secondary"
                                        gutterBottom>
                                {questionNumber}: {question}
                            </Typography>
                            <Typography fontFamily={'Chivo Mono'} variant="h6" fontSize={'18px'} component="div">
                                {selectedModelValue}: {response}
                            </Typography>
                        </CardContent>
                    </Card>
                );
            });

            setFormattedContent(formattedQuestions);
        } catch (error) {
            console.error("Error parsing JSON:", error);
            setFormattedContent('Error');
        }
    }


    const handleJiraConnection = () => {
        axios.get(
            `${BaseURL}get_story_list?api_key=${websiteKey}${userKey}&project_key=${projectKey}&email=${email}&api_token=${jiraAPIkey}`
        ).then((responses) => {
            setJiraArray(responses.data.jira)

        }).catch((error) => {
            console.error("Error:", error);
        }).finally(() => {
            setLoading(false);
        });
    }

    const handleSend = () => {
        setLoading(true);
    
        // Concatenate inputValue and formatDataString if formatDataString exists
        const messageToSend = formatDataString ? inputValue +" Format: "+ formatDataString : inputValue;
    
        setMessages((prev) => [
            ...prev,
            {
                message: messageToSend,
                sender: "You",
            },
        ]);
    
        if (multiLLM) {
            models.forEach(element => {
                axios.get(`${QueryModel}${element.value}&Prompt=${messageToSend}&History=${JSON.stringify(model_history)}`)
                    .then((response) => {
                        setInputValue(''); // Clear the input field
                        setMessages((prev) => [...prev, {
                            message: response.data.model!.response!,
                            sender: `Argo AI - ${element.value}`
                        }]);
                        const temp = modelObject;
                        temp[element.value] = {
                            "model_history": response.data.model!.model_history!
                        };
                        console.log(temp);
                        console.log(`First Message: ${
                            messages.filter(message => message.sender === 'You')[0]?.message
                        }`);
                        setModelObject(temp);
                        setModel_history(response.data.model!.model_history!);
                        console.log(model_history);
                    })
                    .catch(e => {
                        console.log(e);
                    })
                    .finally(() => {
                        setLoading(false);
                    });
            });
        } else {
            axios.get(`${QueryModel}${model}&Prompt=${messageToSend}&History=${JSON.stringify(model_history)}`)
                .then((response) => {
                    setInputValue(''); // Clear the input field
                    setMessages((prev) => [...prev, {
                        message: response.data.model!.response!,
                        sender: `Argo AI - ${model}`
                    }]);
                    const temp = modelObject;
                    temp[model] = {
                        "model_history": response.data.model!.model_history!
                    };
                    console.log(temp);
                    console.log(`First Message: ${
                        messages.filter(message => message.sender === 'You')[0]?.message
                    }`);
                    setModelObject(temp);
                    setModel_history(response.data.model!.model_history!);
    
                    console.log(model_history);
                })
                .finally(() => {
                    setLoading(false);
                });
        }
    };
    


    const handleUpload = () => {
        // Handle the upload action
        console.log('Uploading document');
    };

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(FindPrompts);
                if (!response.ok) {
                    throw new Error('Failed to fetch data');
                }
                const responseData = await response.json();
                setData(responseData);

            } catch (error) {
                console.error('Error fetching data:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [FindPrompts]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(AllFormats);
                if (!response.ok) {
                    throw new Error('Failed to fetch data');
                }
                const responseData = await response.json();
                setData4(responseData.keys);

            } catch (error) {
                console.error('Error fetching data:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [invalidate2]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(AllPrompts);
                if (!response.ok) {
                    throw new Error('Failed to fetch data');
                }
                const responseData = await response.json();
                setData3(responseData.keys);

            } catch (error) {
                console.error('Error fetching data:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [invalidate]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(FindFormats);
                if (!response.ok) {
                    throw new Error('Failed to fetch data');
                }
                const responseData = await response.json();
                setData2(responseData);

            } catch (error) {
                console.error('Error fetching data:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [FindFormats]);
    const [formatSelectionModal, setFormatSelectionModal] = useState(false)
    return (
        <div style={{display: "flex", justifyContent: 'space-between', padding: '1rem', backgroundColor: '#1e7cd3'}}>
            <link rel="preconnect" href="https://fonts.googleapis.com"/>
            <link rel="preconnect" href="https://fonts.gstatic.com"/>
            <link
                href="https://fonts.googleapis.com/css2?family=Noto+Serif:ital,wdth,wght@0,62.5..100,100..900;1,62.5..100,100..900&display=swap"
                rel="stylesheet"/>
            <link href="https://fonts.googleapis.com/css2?family=Aleo:ital,wght@0,100..900;1,100..900&display=swap"
                  rel="stylesheet"/>
            <link
                href="https://fonts.googleapis.com/css2?family=Chivo+Mono:ital,wght@0,100..900;1,100..900&family=Cutive+Mono&display=swap"
                rel="stylesheet"/>
            <div style={{
                maxWidth: '24%',
                width: '24%',
                height: 'calc(100vh - 3rem)',
                borderRadius: '1rem',
                display: "flex",
                flexDirection: "column",
                alignItems: "center"
            }}>
                <div style={{
                    display: 'flex',
                    width: '100%',
                    alignItems: 'center',
                    padding: '10px',
                    paddingLeft: '20px',
                    paddingRight: '25px'
                }}>
                    <a
                        className="pointer-events-none flex place-items-center gap-2 p-8 lg:pointer-events-auto lg:p-0"
                        href="https://argodata.com/"
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        <Image
                            src="/argo.svg"
                            alt="argo logo"
                            style={{filter: 'brightness(0) invert(1)'}}
                            width={140}
                            height={40}
                            priority
                        />
                    </a>
                    <CustomSecondaryButtonWithBackground startIcon={<AddIcon/>}
                                                         sx={{marginLeft: 'auto', marginRight: '5px'}}
                                                         onClick={() => {
                                                             handleOpen()
                                                             console.log(jiraModalOpen)
                                                         }}>
                        Connect to Jira
                    </CustomSecondaryButtonWithBackground>
                </div>
                <div style={{
                    marginBottom: "10px",
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    width: '95%'
                }}>
                    <CustomSecondaryButtonWithBackground onClickCapture={() => {
                        setFormatSelectionModal(true)
                    }}>
                        <SettingsIcon/>
                    </CustomSecondaryButtonWithBackground>
                    <div style={{
                        marginLeft: "20px",
                        marginRight: '5px',
                        display: "flex",
                        justifyContent: "center",
                        alignItems: "center",
                    }}>
                        {/* User Dropdown */}
                        <Typography color={'white'} fontFamily={'Chivo Mono'} fontWeight={700} fontSize={'20px'}>
                            {`Format: ${formatDataString}` || 'Current Format'}
                        </Typography>
                    </div>
                </div>
                <div style={{
                    background: "white",
                    height: 'calc(100% - 100px)',
                    width: '95%',
                    borderRadius: '1rem',
                    marginRight: '1rem',
                    marginBottom: '0.5rem',
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    justifyContent: "center",
                    padding: "10px"
                }}>
                    {jiraArray.length != 0 ?
                        <div style={{height: '250px', overflowY: 'auto'}}>
                            {jiraArray.map((element) => {
                                return (
                                    <Card elevation={0}
                                          sx={{
                                              minWidth: '90%',
                                              marginTop: '10px',
                                              border: '1px solid #000'
                                          }}>
                                        <CardContent>
                                            <Typography fontFamily={'Chivo Mono'} sx={{fontSize: 14}}
                                                        color="text.secondary"
                                                        gutterBottom>
                                                {element[0]}
                                            </Typography>
                                            <Typography fontFamily={'Chivo Mono'} variant="h6"
                                                        fontSize={'18px'} component="div">
                                                {element[1]}
                                            </Typography>
                                        </CardContent>
                                    </Card>
                                )
                            })}
                            <Typography fontFamily={'Chivo Mono'}
                                        sx={{fontSize: 14, textAlign: 'center', marginTop: '10px'}}
                                        color="text.secondary"
                                        gutterBottom>
                                * End of List *
                            </Typography>
                        </div> :
                        <Typography color={'grey'} fontFamily={'Chivo Mono'} fontWeight={300} fontSize={'18px'}
                                    marginLeft={'10px'}>
                            Jira Not Connected
                        </Typography>}
                </div>
                <div style={{
                    marginRight: '5px',
                    marginBottom: "0.5rem",
                    maxWidth: '95%',
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center"
                }}>
                    {/* Title Dropdown */}
                    <label htmlFor="titleDropdown"></label>
                    <Select id="titleDropdown" style={{flex: 1, background: 'white', marginRight: '10px', width: '33%'}}
                            value={PromptTitle} size={'small'}
                            displayEmpty
                            renderValue={(selected: any) => {
                                if (!selected) {
                                    return `Select Title`;
                                }
                                return selected;
                            }} onChange={handleTitleChange}>
                        {data3 && (data3 as string[]).map((title) => (
                            <MenuItem key={title} value={title}>
                                {title}
                            </MenuItem>
                        ))}
                    </Select>
                    <Select id="userDropdown" value={selectedUser}
                            style={{flex: 1, background: 'white', marginRight: '10px', width: '33%'}} size={'small'}
                            displayEmpty
                            renderValue={(selected: any) => {
                                if (!selected) {
                                    return `Select User`;
                                }
                                return selected;
                            }}
                            onChange={handleUserChange}>
                        {usersArray.map((user) => (
                            <MenuItem key={user} value={user}>
                                {user}
                            </MenuItem>
                        ))}
                    </Select>
                    <Select id="modelDropdown" value={models.find(elm => elm.value === selectedModel) && models.find(elm => elm.value === selectedModel)!.label}
                            style={{flex: 1, background: 'white', marginRight: '10px', width: '33%'}} size={'small'}
                            displayEmpty
                            renderValue={(selected: any) => {
                                if (!selected) {
                                    return `Select Model`;
                                }
                                return selected;
                            }} onChange={handleModelChange}>
                        {filteredModels.map((model) => (
                            <MenuItem key={model.value} value={model.value}>
                                {model.label}
                            </MenuItem>
                        ))}
                    </Select>
                </div>
                <div style={{
                    background: "white",
                    height: 'calc(100vh - 100px)',
                    width: '95%',
                    borderRadius: '1rem',
                    marginRight: '1rem',
                    marginBottom: `${user ? '0.5rem' : ''}`,
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    justifyContent: "center",
                    padding: "10px"
                }}>
                    <div style={{height: '250px', overflowY: 'auto'}}>
                        <Typography color={'grey'} fontFamily={'Chivo Mono'} fontWeight={300} fontSize={'18px'}>
                            {formattedContent || 'Previous Chat History'}
                        </Typography>
                        {formattedContent && <Typography fontFamily={'Chivo Mono'}
                                     sx={{fontSize: 14, textAlign: 'center', marginTop: '10px'}}
                                     color="text.secondary"
                                     gutterBottom>
                            * End of List *
                        </Typography>}
                    </div>
                    {formattedContent &&
                        <div style={{
                            display: "flex",
                            marginTop: "auto",
                            marginBottom: '1px',
                            width: '100%'
                        }}>
                            <PrimaryButtonWithBackground disabled={!formattedContent} onClick={() => {
                                setMessages([])
                                setModel(selectedModel)
                                setModel_history(samplehistory)
                                let messagesArray: any[] = []
                                const formattedQuestions = Object.keys(samplehistory).map((key: any) => {
                                    const questionNumber = key.replace("_", " ");
                                    const question = samplehistory[key][0];
                                    const response = samplehistory[key][1];
                                    messagesArray.push({
                                        message: question,
                                        sender: "You",
                                    }, {
                                        message: response,
                                        sender: `Argo AI - ${selectedModel}`
                                    })

                                });
                                setMessages(messagesArray)
                            }} sx={{marginLeft: 'auto', marginRight: '5px'}}>
                                <SwapCallsIcon/>
                            </PrimaryButtonWithBackground>
                            <DestructiveButtonWithBackground
                                disabled={false}
                                sx={{marginRight: '1px'}}
                                onClickCapture={async () => {
                                    try {
                                        await fetch(`${BaseURL}RemovePrompt?api_key=${websiteKey}${userKey}&Username=${username}&Title=${PromptTitle}`);
                                        window.location.reload();
                                    } catch (error) {
                                        console.error('Error fetching data:', error);
                                    }
                                }}
                            >
                                <DeleteIcon/>
                            </DestructiveButtonWithBackground>

                        </div>}
                </div>
                {
                    user &&
                    <div style={{
                        flex: '1',
                        display: 'flex',
                        background: "white",
                        width: '92%',
                        borderRadius: '1rem',
                        marginRight: '1rem',
                        flexDirection: 'column',
                        alignItems: 'center',
                        justifyContent: 'center',
                        padding: '10px',
                        paddingLeft: '20px',
                    }}>
                        {user ? (
                            <div style={{display: 'flex', alignItems: 'center'}}>
                                <img src={user!.picture!} alt={user!.name!}
                                     style={{marginRight: '10px', borderRadius: '50%', height: '50px'}}/>
                                <div>
                                    <h3 style={{margin: 0}}>{username}</h3>
                                    <p style={{margin: 0, textAlign: 'center'}}>{user.email}</p>

                                </div>

                            </div>
                        ) : (
                            <div style={{flex: '1'}}></div>
                        )}
                    </div>
                }
            </div>


            <div style={{
                width: '76%',
                background: "white",
                height: 'calc(100vh - 3rem)',
                borderRadius: '1rem',
                overflowY: "hidden"
            }}>
                <div style={{
                    height: '60px',
                    position: "sticky",
                    top: 0, left: 0,
                    background: '#fff',
                    display: "flex",
                    paddingLeft: '30px',
                    paddingRight: '20px',
                    alignItems: "center",
                    borderBottom: "2px solid #E0E0E0", // Add a bottom border
                    boxShadow: "0px 4px 6px rgba(0, 0, 0, 0.09)" // Add a drop shadow
                }}>
                    <Typography fontFamily={'Chivo Mono'} fontWeight={500} fontSize={'18px'}>AI Chat
                        Helper </Typography>


                    <div>

                    </div>


                    <div style={{
                        marginLeft: "auto",
                        marginRight: '0px',
                        display: "flex",
                        justifyContent: "center",
                        alignItems: "center"
                    }}>
                        <AppInputBox 
    onChange={(event) => {
        setPTitle(event.target.value);
    }}
    placeholder="Set Prompt Title"
    sx={{marginRight: '10px', width: '200px'}}
    value={PTitle} // Assuming PTitle is the state variable for the prompt title
/>

                        <AppInputBox
                            onChange={(event) => {
                                setUserKey(event.target.value)
                            }}
                            placeholder="User password"
                            type={showPassword ? 'text' : 'password'}
                            endAdornment={
                                <InputAdornment position="end">
                                    <IconButton
                                        aria-label="toggle password visibility"
                                        onClick={handleClickShowPassword}
                                        onMouseDown={handleMouseDownPassword}
                                        edge="end"
                                    >
                                        {showPassword ? <VisibilityOff/> : <Visibility/>}
                                    </IconButton>
                                </InputAdornment>
                            }
                            sx={{marginRight: '10px', width: '200px'}}
                            value={userKey}
                        />
                        <CustomButtonWithOutline startIcon={<CloseIcon/>} onClickCapture={() => {
                            setMessages([]);
                            setModel_history({});
                            setLoading(false);
                        }} sx={{marginLeft: '10px'}}
                                                 onClick={handleUpload}>
                            Clear Chat
                        </CustomButtonWithOutline>
                        <CustomButtonWithOutline startIcon={<SaveAlt/>} disabled={messages.length == 0}
                                                 onClickCapture={() => {
                                                     setPTitleUUID(uuidv4())
                                                     const jsonPromptExample: any = {
                                                        [PTitle ? PTitle : username + pTitleUUID]: {
                                                             [username]: {
                                                                 "Prompt": messages[0].message,
                                                                 "SDLC": SDLCNum,
                                                                 "Security": secNum,
                                                                 "models": {
                                                                     [model]: {
                                                                         model_history
                                                                     }
                                                                 }
                                                             }
                                                         }
                                                     };
                                                     const fetchData = async () => {
                                                         try {
                                                             const response = await fetch(`${BaseURL}AddPrompt?api_key=${websiteKey}${userKey}&Data=${JSON.stringify(jsonPromptExample)}`);
                                                             console.log(response)
                                                         } catch (error) {
                                                             console.error('Error fetching data:', error);
                                                         } finally {
                                                             setLoading(false);
                                                         }
                                                     };

                                                     fetchData().then().finally(() => {
                                                         setInvalidate(!invalidate);
                                                     });


                                                 }} sx={{marginLeft: '10px'}}>
                            Save Chat History
                        </CustomButtonWithOutline>

                        {user ? (
                            <CustomButtonWithOutline href="/api/auth/logout" sx={{marginLeft: '10px'}}>
                                Logout
                            </CustomButtonWithOutline>
                        ) : (
                            <CustomButtonWithOutline href="/api/auth/login" sx={{marginLeft: '10px'}}>
                                Login
                            </CustomButtonWithOutline>
                        )}
                    </div>
                </div>
                <div>
                    <div>
                        {multiLLM && <Tabs value={currentTab}>
                            {models.map((element, index) =>
                                <Tab key={index} label={element.label} value={element.value}
                                     onClick={() => setCurrentTab(element.value)}/>
                            )}
                        </Tabs>}
                    </div>
                    <div className={messages.length === 0 ? 'no-content' : ''}
                         style={{
                             height: multiLLM ? 'calc(100vh - 265px)' : 'calc(100vh - 225px)',
                             background: 'white',
                             padding: '20px',
                             overflow: "auto"
                         }}>
                        {!multiLLM && messages.map((message, index) => (
                            <ChatBubble key={index} text={message.message} sender={message.sender}/>
                        ))}
                        {multiLLM && messages.filter(message => message.sender.includes(currentTab) || message.sender === 'You')
                            .map((message, index) => (
                                <ChatBubble key={index} text={message.message} sender={message.sender}/>
                            ))}
                        {messages.length === 0 && <div>
                            <Typography color={'grey'} fontFamily={'Chivo Mono'} fontWeight={300} fontSize={'18px'}>How
                                can
                                I help you today?</Typography>
                        </div>}
                        {
                            loading && <div style={{paddingTop: '20px'}}>
                                <Typography textAlign={'right'} color={'grey'} fontFamily={'Chivo Mono'}
                                            fontWeight={300} fontSize={'15px'}>Argo AI</Typography>
                                <div className={'chat-bubble-response'}>
                                    <Skeleton animation="wave"/>
                                    <Skeleton animation="wave"/>
                                    <Skeleton animation="wave"/>
                                </div>
                                {multiLLM && <div ref={refToMonitor}/>}
                            </div>
                        }
                        {!multiLLM && <div ref={refToMonitor}/>}
                    </div>
                    <div
                        style={{
                            position: 'sticky',
                            bottom: 0,
                            left: 0,
                            background: 'white',
                            display: 'flex',
                            alignItems: 'center',
                            paddingLeft: '15px',
                            paddingRight: '15px',
                            paddingTop: '10px',
                            paddingBottom: '10px',
                            zIndex: 1000,
                            marginTop: multiLLM ? '50px' : ''
                        }}
                    >
                        <CustomButton startIcon={<UploadFileIcon/>} sx={{marginRight: '10px'}} disabled
                                      onClick={handleUpload}>
                            Upload
                        </CustomButton>
                        <CustomButtonWithBackground
                            sx={{marginRight: '10px', width: '20%'}}
                            id="basic-button"
                            aria-controls={open ? 'basic-menu' : undefined}
                            aria-haspopup="true"
                            aria-expanded={open ? 'true' : undefined}
                            onClick={handleClick}
                        >
                            {!multiLLM ? models.find(element => element.value === model)!.label : 'Multi LLM'}
                        </CustomButtonWithBackground>
                        <Menu
                            id="basic-menu"
                            anchorEl={anchorEl}
                            open={open}
                            onClose={() => {
                                setAnchorEl(null);
                            }}
                            MenuListProps={{
                                'aria-labelledby': 'basic-button',
                            }}
                        >
                            {models.map((element, index) =>
                                <MenuItem key={index} onClick={() => {
                                    setModel(element.value)
                                    setMultiLLM(false)
                                    setAnchorEl(null);
                                }}>{element.label}</MenuItem>
                            )}
                            <MenuItem onClick={() => {
                                setMultiLLM(true)
                                setAnchorEl(null);
                            }}>Multi LLM</MenuItem>
                        </Menu>
                        <AppInputBox
                            fullWidth
                            multiline
                            maxRows={5}
                            value={inputValue}
                            onChange={handleChange}
                            placeholder="Type a message..."
                            sx={{marginRight: '10px'}}
                            disabled={loading || userKey.length != 10}
                        />
                        <HeroButtonWithBackground disabled={loading || userKey.length != 10} onClick={handleSend}>
                            <SendRoundedIcon/>
                        </HeroButtonWithBackground>
                        <Modal
                            open={jiraModalOpen}
                            onClose={handleClose}
                        >
                            <Box sx={style}>
                                <div style={{display: 'flex', justifyContent: 'space-around', alignItems: 'center'}}>
                                    <Typography id="modal-modal-description" sx={{mr: 2, flex: 1}}>
                                        Email
                                    </Typography>
                                    <AppInputBox
                                        fullWidth
                                        sx={{flex: 2}}
                                        value={email}
                                        onChange={(event: any) => {
                                            setEmail(event.target.value);
                                        }}
                                        placeholder="Type your email"
                                        disabled={loading || userKey.length != 10}
                                    />
                                </div>
                                <div style={{
                                    display: 'flex',
                                    justifyContent: 'space-around',
                                    alignItems: 'center',
                                    marginTop: '10px'
                                }}>
                                    <Typography id="modal-modal-description" sx={{mr: 2, flex: 1}}>
                                        Project Key
                                    </Typography>
                                    <AppInputBox
                                        fullWidth
                                        sx={{flex: 2}}
                                        value={projectKey}
                                        onChange={(event: any) => {
                                            setProjectKey(event.target.value);
                                        }}
                                        placeholder="Type the project key"
                                        disabled={loading || userKey.length != 10}
                                    />
                                </div>
                                {jiraArray.length > 0 &&
                                    <div style={{marginTop: '20px', marginBottom: '10px',}}>
                                        <Typography fontFamily={'Chivo Mono'} variant="h6" fontSize={'20px'}
                                                    component="div">
                                            Current Jira List
                                        </Typography>
                                        <div style={{height: '250px', overflowY: 'auto'}}>
                                            {jiraArray.map((element) => {
                                                return (
                                                    <Card elevation={0}
                                                          sx={{
                                                              minWidth: 275,
                                                              marginTop: '10px',
                                                              border: '1px solid #000'
                                                          }}>
                                                        <CardContent>
                                                            <Typography fontFamily={'Chivo Mono'} sx={{fontSize: 14}}
                                                                        color="text.secondary"
                                                                        gutterBottom>
                                                                {element[0]}
                                                            </Typography>
                                                            <Typography fontFamily={'Chivo Mono'} variant="h6"
                                                                        fontSize={'18px'} component="div">
                                                                {element[1]}
                                                            </Typography>
                                                        </CardContent>
                                                    </Card>
                                                )
                                            })}
                                        </div>
                                    </div>
                                }
                                <CustomButtonWithBackground sx={{float: 'right', marginTop: '10px'}}
                                                            onClick={() => {
                                                                handleClose()
                                                                handleJiraConnection();
                                                            }}>
                                    Connect to Jira
                                </CustomButtonWithBackground>
                            </Box>
                        </Modal>
                        <Modal
                            open={formatSelectionModal}
                            onClose={() => {
                                setFormatSelectionModal(false)
                            }}
                        >
                            <Box sx={style}>
                                <Typography fontFamily={'Chivo Mono'} variant="h6" fontSize={'25px'} component="div"
                                            sx={{mb: 1}}>
                                    Options
                                </Typography>

<Typography fontFamily={'Chivo Mono'} variant="h6" fontSize={'15px'} component="div"
                                            sx={{mb: 1, marginTop: '10px'}}>
Security For New Prompt:
<AppInputBox 
    onChange={(event) => {
        setSecNum(event.target.value);
    }}
    sx={{marginRight: '10px', width: '40px'}}
    value={secNum} 
/>
</Typography>
<Typography fontFamily={'Chivo Mono'} variant="h6" fontSize={'15px'} component="div"
                                            sx={{mb: 1, marginTop: '10px'}}>
SDLC For New Prompt:
<AppInputBox 
    onChange={(event) => {
        setSDLCNum(event.target.value);
    }}
    sx={{marginRight: '10px', width: '40px'}}
    value={SDLCNum} 
/>
</Typography>
<Typography fontFamily={'Chivo Mono'} variant="h6" fontSize={'25px'} component="div"
                                            sx={{mb: 1, marginTop: '10px'}}>
                                    Format Selection
                                </Typography>
                                <div style={{display: 'flex', justifyContent: 'space-around', alignItems: 'center'}}>
                                <label htmlFor="titleDropdown"></label>
                    <Select id="ftitleDropdown" style={{flex: 1, background: 'white', marginRight: '10px', width: '33%'}}
                    
                            value={FormatTitle} size={'small'}
                            displayEmpty
                            renderValue={(selected: any) => {
                                if (!selected) {
                                    return `Select Title`;
                                }
                                return selected;
                            }} onChange={handleTitleChange2}>
                        {data4 && (data4 as string[]).map((title) => (
                            <MenuItem key={title} value={title}>
                                {title}
                            </MenuItem>
                        ))}
                    </Select>
                                    <Select id="userDropdown2" displayEmpty size={"small"} value={selectedUser2}
                                            renderValue={(selected: any) => {
                                                if (!selected) {
                                                    return `Select User`;
                                                }
                                                return selected;
                                            }} onChange={handleUserChange2}
                                            sx={{background: 'white', marginLeft: '10px'}}>
                                        {usersArray2.map((user2) => (
                                            <MenuItem key={user2} value={user2}>
                                                {user2}
                                            </MenuItem>
                                        ))}
                                    </Select>
                                    <Typography color={'black'} fontFamily={'Chivo Mono'} fontWeight={300}
                                                fontSize={'15px'}
                                                marginLeft={'10px'}>
                                        {`Selected format: ${formatDataString}` || 'No Format Selected'}




                                    </Typography>
                                </div>
                                <AppInputBox 
    onChange={(event) => {
        setFformat(event.target.value);
        const words = event.target.value.trim().split(" ");
        setFTitle(words[words.length - 1]);
    }}
    placeholder="Set Format"
    endAdornment={
        <InputAdornment position="end">
            <IconButton
                aria-label="Create New Format"
                onClickCapture={() => {
                    

                    const jsonFormatExample = {
                        [FTitle]: {
                            [username]: Fformat
                        }
                    };
                    const fetchData = async () => {
                        try {
                            const response = await fetch(`${BaseURL}AddFormat?api_key=${websiteKey}${userKey}&Data=${JSON.stringify(jsonFormatExample)}`);
                            console.log(response);
                        } catch (error) {
                            console.error('Error fetching data:', error);
                        } finally {
                            setLoading(false);
                            setFformat(""); // Clear the input box
                        }
                    };

                    fetchData().then().finally(() => {
                        setInvalidate2(!invalidate2);
                    });
                }}
                onMouseDown={handleMouseDownPassword}
                edge="end"
                sx={{marginLeft: '10px'}}
            >
                
                <SendRoundedIcon/>
            </IconButton>
        </InputAdornment>
    }
    sx={{marginRight: '10px', width: '200px'}}
    value={Fformat}
/>
                            </Box>
                        </Modal>
                    </div>
                </div>
            </div>
        </div>
    );
}

const useAutoScroll = (elementRef: any) => {
    const [hasScrolled, setHasScrolled] = useState(false);

    useEffect(() => {
        const observer = new IntersectionObserver(
            (entries) => {
                const entry = entries[0];
                if (!entry.isIntersecting && !hasScrolled) {
                    elementRef.current.scrollIntoView({behavior: 'smooth'});
                }
            },
            {threshold: 0.1}
        );

        if (elementRef.current) {
            observer.observe(elementRef.current);
        }

        const handleScroll = () => {
            setHasScrolled(true);
        };

        window.addEventListener('scroll', handleScroll);

        return () => {
            observer.disconnect();
            window.removeEventListener('scroll', handleScroll);
        };
    }, [elementRef, hasScrolled]);

    return {hasScrolled};
};
